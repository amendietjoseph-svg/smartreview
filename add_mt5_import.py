import re, glob

# 1. Ajouter endpoint backend pour import MT5
mt5_router = '''"""
MT5/MT4 Trade Import Router
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Trade
import csv
import io
from datetime import datetime

router = APIRouter()

def parse_mt5_csv(content: str, account_id: int):
    """Parse MT5 history export CSV"""
    trades = []
    lines = content.strip().split("\\n")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("Time"):
            continue
        
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 10:
            continue
            
        try:
            # MT5 format: #,Time,Deal,Symbol,Type,Direction,Volume,Price,Order,Commission,Swap,Profit,Balance
            trade_type = parts[4].lower() if len(parts) > 4 else ""
            direction = parts[5].lower() if len(parts) > 5 else ""
            
            if direction not in ["in", "out"] and trade_type not in ["buy", "sell"]:
                continue
                
            if direction == "out" or (trade_type in ["buy", "sell"] and direction == "out"):
                profit = float(parts[11]) if len(parts) > 11 else 0
                volume = float(parts[6]) if len(parts) > 6 else 0
                price = float(parts[7]) if len(parts) > 7 else 0
                symbol = parts[3] if len(parts) > 3 else ""
                commission = float(parts[9]) if len(parts) > 9 else 0
                swap = float(parts[10]) if len(parts) > 10 else 0
                
                time_str = parts[1] if len(parts) > 1 else ""
                try:
                    trade_time = datetime.strptime(time_str, "%Y.%m.%d %H:%M:%S")
                except:
                    try:
                        trade_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    except:
                        trade_time = datetime.now()
                
                trade = {
                    "account_id": account_id,
                    "asset": symbol,
                    "direction": "BUY" if trade_type == "buy" else "SELL",
                    "entry_price": price,
                    "exit_price": price,
                    "lot_size": volume,
                    "profit_loss": profit,
                    "result": "WIN" if profit > 0 else "LOSS" if profit < 0 else "BREAKEVEN",
                    "trade_date": trade_time.strftime("%Y-%m-%d"),
                    "entry_time": trade_time.strftime("%H:%M:%S"),
                    "risk_amount": abs(commission),
                    "notes": f"Import MT5 | Commission: {commission} | Swap: {swap}"
                }
                trades.append(trade)
        except Exception as e:
            continue
    
    return trades

def parse_mt4_csv(content: str, account_id: int):
    """Parse MT4 history export CSV"""
    trades = []
    lines = content.strip().split("\\n")
    
    for line in lines:
        line = line.strip()
        if not line or "#" in line[:5] or "Ticket" in line:
            continue
            
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 10:
            continue
            
        try:
            # MT4 format: Ticket,Open Time,Type,Size,Item,Price,S/L,T/P,Close Time,Close Price,Commission,Swap,Profit
            ticket = parts[0]
            open_time_str = parts[1] if len(parts) > 1 else ""
            trade_type = parts[2].lower() if len(parts) > 2 else ""
            size = float(parts[3]) if len(parts) > 3 else 0
            symbol = parts[4] if len(parts) > 4 else ""
            open_price = float(parts[5]) if len(parts) > 5 else 0
            sl = float(parts[6]) if len(parts) > 6 and parts[6] else 0
            tp = float(parts[7]) if len(parts) > 7 and parts[7] else 0
            close_price = float(parts[9]) if len(parts) > 9 else 0
            commission = float(parts[10]) if len(parts) > 10 else 0
            swap = float(parts[11]) if len(parts) > 11 else 0
            profit = float(parts[12]) if len(parts) > 12 else 0
            
            if trade_type not in ["buy", "sell"]:
                continue
            
            try:
                trade_time = datetime.strptime(open_time_str, "%Y.%m.%d %H:%M:%S")
            except:
                try:
                    trade_time = datetime.strptime(open_time_str, "%Y-%m-%d %H:%M:%S")
                except:
                    trade_time = datetime.now()
            
            trade = {
                "account_id": account_id,
                "asset": symbol,
                "direction": "BUY" if trade_type == "buy" else "SELL",
                "entry_price": open_price,
                "exit_price": close_price,
                "stop_loss": sl if sl > 0 else None,
                "take_profit": tp if tp > 0 else None,
                "lot_size": size,
                "profit_loss": profit,
                "result": "WIN" if profit > 0 else "LOSS" if profit < 0 else "BREAKEVEN",
                "trade_date": trade_time.strftime("%Y-%m-%d"),
                "entry_time": trade_time.strftime("%H:%M:%S"),
                "notes": f"Import MT4 | Ticket: {ticket} | Commission: {commission} | Swap: {swap}"
            }
            trades.append(trade)
        except Exception as e:
            continue
    
    return trades

@router.post("/mt5")
async def import_mt5(
    file: UploadFile = File(...),
    account_id: int = 1,
    db: Session = Depends(get_db)
):
    """Import trades from MT5 CSV export"""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    
    # Auto-detect MT4 vs MT5
    if "Deal" in text[:500] or "Direction" in text[:500]:
        trades_data = parse_mt5_csv(text, account_id)
        format_used = "MT5"
    else:
        trades_data = parse_mt4_csv(text, account_id)
        format_used = "MT4"
    
    if not trades_data:
        raise HTTPException(status_code=400, detail="No valid trades found in file")
    
    imported = 0
    for trade_data in trades_data:
        try:
            trade = Trade(**{k: v for k, v in trade_data.items() if v is not None})
            db.add(trade)
            db.commit()
            imported += 1
        except Exception as e:
            db.rollback()
            continue
    
    return {
        "success": True,
        "format": format_used,
        "imported": imported,
        "total": len(trades_data),
        "message": f"{imported} trades importés depuis {format_used}"
    }

@router.post("/csv")
async def import_csv(
    file: UploadFile = File(...),
    account_id: int = 1,
    db: Session = Depends(get_db)
):
    """Import trades from generic CSV"""
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    
    # Try MT5 first, then MT4
    trades_data = parse_mt5_csv(text, account_id)
    if not trades_data:
        trades_data = parse_mt4_csv(text, account_id)
    
    if not trades_data:
        raise HTTPException(status_code=400, detail="Format non reconnu")
    
    imported = 0
    for trade_data in trades_data:
        try:
            trade = Trade(**{k: v for k, v in trade_data.items() if v is not None})
            db.add(trade)
            db.commit()
            imported += 1
        except:
            db.rollback()
            continue
    
    return {"success": True, "imported": imported, "total": len(trades_data)}
'''

with open('backend/routers/import_trades.py', 'w', encoding='utf-8') as f:
    f.write(mt5_router)
print('import_trades.py created!')

# 2. Ajouter le router dans main.py
with open('backend/main.py', 'r', encoding='utf-8') as f:
    c = f.read()

if 'import_trades' not in c:
    c = c.replace(
        'from routers import trades, stats, accounts, ai_coach, auth',
        'from routers import trades, stats, accounts, ai_coach, auth, import_trades'
    )
    c = c.replace(
        'app.include_router(auth.router, prefix="/api/auth", tags=["auth"])',
        'app.include_router(auth.router, prefix="/api/auth", tags=["auth"])\napp.include_router(import_trades.router, prefix="/api/import", tags=["import"])'
    )
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(c)
    print('main.py updated!')

# 3. Ajouter interface import dans journal.html
with open('frontend/journal.html', 'r', encoding='utf-8') as f:
    c = f.read()

import_ui = """
<style id="import-style">
.import-modal {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.8);
  backdrop-filter: blur(4px);
  z-index: 1000;
  align-items: center;
  justify-content: center;
}
.import-modal.active { display: flex; }
.import-box {
  background: #1e222d;
  border: 1px solid #2a2e39;
  border-radius: 20px;
  padding: 32px;
  width: 90%;
  max-width: 500px;
}
.import-title {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}
.import-subtitle {
  font-size: 13px;
  color: #787b86;
  margin-bottom: 24px;
}
.import-dropzone {
  border: 2px dashed #2a2e39;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 16px;
}
.import-dropzone:hover, .import-dropzone.dragover {
  border-color: #26a69a;
  background: rgba(38,166,154,0.05);
}
.import-dropzone svg { color: #787b86; margin-bottom: 12px; }
.import-dropzone p { color: #787b86; font-size: 13px; }
.import-dropzone strong { color: #26a69a; }
.import-format-btns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 16px;
}
.format-btn {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #2a2e39;
  background: #131722;
  color: #787b86;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.15s;
  text-align: center;
}
.format-btn.active {
  border-color: #26a69a;
  color: #26a69a;
  background: rgba(38,166,154,0.1);
}
.import-account-select {
  width: 100%;
  background: #131722;
  border: 1px solid #2a2e39;
  border-radius: 8px;
  color: #fff;
  padding: 10px 12px;
  font-size: 13px;
  margin-bottom: 16px;
  font-family: Inter, sans-serif;
}
.import-actions {
  display: flex;
  gap: 10px;
}
.import-btn {
  flex: 1;
  padding: 12px;
  background: linear-gradient(135deg, #26a69a, #1a8a7e);
  color: #000;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}
.import-cancel {
  padding: 12px 20px;
  background: #1a1a1a;
  border: 1px solid #2a2e39;
  color: #787b86;
  border-radius: 10px;
  font-size: 13px;
  cursor: pointer;
}
.import-progress {
  display: none;
  margin-top: 16px;
  padding: 12px;
  background: rgba(38,166,154,0.1);
  border: 1px solid rgba(38,166,154,0.3);
  border-radius: 8px;
  font-size: 13px;
  color: #26a69a;
  text-align: center;
}
.import-result {
  display: none;
  margin-top: 16px;
  padding: 12px;
  border-radius: 8px;
  font-size: 13px;
  text-align: center;
}
.import-result.success {
  background: rgba(38,166,154,0.1);
  border: 1px solid rgba(38,166,154,0.3);
  color: #26a69a;
}
.import-result.error {
  background: rgba(239,83,80,0.1);
  border: 1px solid rgba(239,83,80,0.3);
  color: #ef5350;
}
</style>

<!-- IMPORT MODAL -->
<div class="import-modal" id="importModal">
  <div class="import-box">
    <div class="import-title">📥 Importer des Trades</div>
    <div class="import-subtitle">Importez votre historique depuis MT4, MT5 ou un fichier CSV</div>
    
    <div class="import-format-btns">
      <div class="format-btn active" onclick="selectFormat(this,'mt5')">📊 MT5</div>
      <div class="format-btn" onclick="selectFormat(this,'mt4')">📈 MT4</div>
    </div>
    
    <select class="import-account-select" id="importAccountId">
      <option value="1">Chargement des comptes...</option>
    </select>
    
    <div class="import-dropzone" id="importDropzone" onclick="document.getElementById('importFileInput').click()">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin:0 auto 12px;display:block;">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
        <polyline points="17 8 12 3 7 8"/>
        <line x1="12" y1="3" x2="12" y2="15"/>
      </svg>
      <p>Glissez votre fichier ici ou <strong>cliquez pour parcourir</strong></p>
      <p style="font-size:11px;margin-top:6px;">Fichiers CSV acceptés (MT4/MT5 History Export)</p>
    </div>
    <input type="file" id="importFileInput" accept=".csv" style="display:none">
    
    <div class="import-progress" id="importProgress">⏳ Import en cours...</div>
    <div class="import-result" id="importResult"></div>
    
    <div class="import-actions">
      <button class="import-cancel" onclick="closeImportModal()">Annuler</button>
      <button class="import-btn" onclick="startImport()">📥 Importer</button>
    </div>
  </div>
</div>

<script id="import-script">
const IMPORT_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8001'
  : 'https://smartreview-y4sq.onrender.com';

let selectedFormat = 'mt5';
let selectedFile = null;

function selectFormat(btn, format) {
  document.querySelectorAll('.format-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  selectedFormat = format;
}

function openImportModal() {
  document.getElementById('importModal').classList.add('active');
  // Charger les comptes
  fetch(IMPORT_BASE + '/api/accounts/')
    .then(r => r.json())
    .then(accounts => {
      const sel = document.getElementById('importAccountId');
      if(accounts && accounts.length > 0) {
        sel.innerHTML = accounts.map(a => 
          `<option value="${a.id}">${a.name}</option>`
        ).join('');
      } else {
        sel.innerHTML = '<option value="1">Compte par défaut</option>';
      }
    })
    .catch(() => {
      document.getElementById('importAccountId').innerHTML = '<option value="1">Compte par défaut</option>';
    });
}

function closeImportModal() {
  document.getElementById('importModal').classList.remove('active');
  selectedFile = null;
  document.getElementById('importFileInput').value = '';
  document.getElementById('importProgress').style.display = 'none';
  document.getElementById('importResult').style.display = 'none';
}

// Drag and drop
const dropzone = document.getElementById('importDropzone');
if(dropzone) {
  dropzone.addEventListener('dragover', e => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
  dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if(file) handleFile(file);
  });
}

document.getElementById('importFileInput')?.addEventListener('change', function() {
  if(this.files[0]) handleFile(this.files[0]);
});

function handleFile(file) {
  selectedFile = file;
  const dropzone = document.getElementById('importDropzone');
  dropzone.innerHTML = `
    <div style="color:#26a69a;font-size:24px;margin-bottom:8px;">✓</div>
    <p style="color:#26a69a;font-weight:600;">${file.name}</p>
    <p style="font-size:11px;color:#787b86;">${(file.size/1024).toFixed(1)} KB</p>
  `;
}

async function startImport() {
  if(!selectedFile) {
    alert('Veuillez sélectionner un fichier CSV');
    return;
  }
  
  const accountId = document.getElementById('importAccountId').value;
  const progress = document.getElementById('importProgress');
  const result = document.getElementById('importResult');
  
  progress.style.display = 'block';
  result.style.display = 'none';
  
  const formData = new FormData();
  formData.append('file', selectedFile);
  formData.append('account_id', accountId);
  
  try {
    const res = await fetch(`${IMPORT_BASE}/api/import/mt5?account_id=${accountId}`, {
      method: 'POST',
      body: formData
    });
    
    const data = await res.json();
    progress.style.display = 'none';
    
    if(res.ok) {
      result.className = 'import-result success';
      result.style.display = 'block';
      result.innerHTML = `✓ ${data.imported} trades importés depuis ${data.format}`;
      setTimeout(() => {
        closeImportModal();
        window.location.reload();
      }, 2000);
    } else {
      result.className = 'import-result error';
      result.style.display = 'block';
      result.innerHTML = '✗ ' + (data.detail || 'Erreur lors de l\\'import');
    }
  } catch(e) {
    progress.style.display = 'none';
    result.className = 'import-result error';
    result.style.display = 'block';
    result.innerHTML = '✗ Erreur réseau: ' + e.message;
  }
}
</script>"""

import re
c = re.sub(r'<style id="import-style">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', import_ui + '</body>')

# Ajouter bouton Import dans le header du journal
if 'Importer' not in c:
    c = c.replace(
        'id="newTradeBtn"',
        'id="newTradeBtn" style="margin-right:8px;"'
    )
    c = c.replace(
        '+ Nouveau Trade',
        '+ Nouveau Trade</button>\n<button onclick="openImportModal()" style="display:flex;align-items:center;gap:6px;padding:8px 14px;background:rgba(38,166,154,0.15);border:1px solid rgba(38,166,154,0.3);color:#26a69a;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;">📥 Importer MT4/MT5'
    )

with open('frontend/journal.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('journal.html updated!')
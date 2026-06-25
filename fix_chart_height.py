import re

with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix la fonction initChart pour prendre toute la hauteur
old_init = """function initChart() {
        const container = document.getElementById('chart-container');
        if(chart) { chart.remove(); chart = null; }
        
        chart = LightweightCharts.createChart(container, {
            width: container.clientWidth,
            height: container.clientHeight || 500,"""

new_init = """function initChart() {
        const container = document.getElementById('chart-container');
        if(chart) { chart.remove(); chart = null; }
        
        // Forcer la hauteur correcte
        const topbar = document.querySelector('.chart-topbar');
        const balbar = document.querySelector('.balance-bar');
        const totalH = window.innerHeight - 60; // minus navbar
        const usedH = (topbar ? topbar.offsetHeight : 44) + (balbar ? balbar.offsetHeight : 32);
        const chartH = Math.max(300, totalH - usedH - 48); // 48 = bottom bar
        
        chart = LightweightCharts.createChart(container, {
            width: container.clientWidth || 800,
            height: chartH,"""

if old_init in c:
    c = c.replace(old_init, new_init)
    print('initChart fixed!')
else:
    # Chercher et remplacer autrement
    c = re.sub(
        r'height: container\.clientHeight \|\| 500,',
        'height: Math.max(300, window.innerHeight - 200),',
        c
    )
    print('height fallback fixed!')

# Fix resize observer
c = c.replace(
    'chart.applyOptions({ width:container.clientWidth, height:container.clientHeight });',
    '''const tb = document.querySelector('.chart-topbar');
            const bb = document.querySelector('.balance-bar');
            const h = Math.max(300, window.innerHeight - 60 - (tb?tb.offsetHeight:44) - (bb?bb.offsetHeight:32) - 48);
            chart.applyOptions({ width:container.clientWidth, height:h });'''
)

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')

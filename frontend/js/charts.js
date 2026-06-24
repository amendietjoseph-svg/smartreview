/**
 * Chart utilities for SmartFX-Review
 * Uses ApexCharts for all visualizations
 */

/**
 * Render an area chart (equity curve)
 */
function renderAreaChart(elementId, categories, series, title, color = '#3B82F6') {
    const element = document.getElementById(elementId);
    if (!element) return;

    const options = {
        series: [{
            name: title,
            data: series
        }],
        chart: {
            type: 'area',
            height: 300,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        colors: [color],
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth',
            width: 2
        },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.7,
                opacityTo: 0.1,
                stops: [0, 90, 100]
            }
        },
        xaxis: {
            categories: categories,
            labels: {
                style: {
                    colors: '#8B9AB1',
                    fontSize: '12px'
                }
            },
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#8B9AB1',
                    fontSize: '12px'
                },
                formatter: (value) => {
                    return '$' + value.toFixed(2);
                }
            }
        },
        grid: {
            borderColor: '#1E2330',
            strokeDashArray: 4
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: (value) => {
                    return '$' + value.toFixed(2);
                }
            }
        }
    };

    const chart = new ApexCharts(element, options);
    chart.render();
    return chart;
}

/**
 * Render a bar chart
 */
function renderBarChart(elementId, categories, series, title, colors = ['#00D26A', '#3B82F6']) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const options = {
        series: [{
            name: title,
            data: series
        }],
        chart: {
            type: 'bar',
            height: 300,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        colors: colors,
        plotOptions: {
            bar: {
                borderRadius: 4,
                columnWidth: '60%'
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: categories,
            labels: {
                style: {
                    colors: '#8B9AB1',
                    fontSize: '12px'
                },
                rotate: -45,
                rotateAlways: true
            },
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#8B9AB1',
                    fontSize: '12px'
                }
            }
        },
        grid: {
            borderColor: '#1E2330',
            strokeDashArray: 4
        },
        tooltip: {
            theme: 'dark'
        }
    };

    const chart = new ApexCharts(element, options);
    chart.render();
    return chart;
}

/**
 * Render a line chart
 */
function renderLineChart(elementId, categories, series, title) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const options = {
        series: [{
            name: title,
            data: series
        }],
        chart: {
            type: 'line',
            height: 300,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        colors: ['#8B5CF6'],
        stroke: {
            curve: 'smooth',
            width: 2
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: categories,
            labels: {
                style: {
                    colors: '#8B9AB1',
                    fontSize: '12px'
                }
            },
            axisBorder: {
                show: false
            },
            axisTicks: {
                show: false
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#8B9AB1',
                    fontSize: '12px'
                }
            }
        },
        grid: {
            borderColor: '#1E2330',
            strokeDashArray: 4
        },
        tooltip: {
            theme: 'dark'
        }
    };

    const chart = new ApexCharts(element, options);
    chart.render();
    return chart;
}

/**
 * Render a donut chart
 */
function renderDonutChart(elementId, labels, series, title) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const options = {
        series: series,
        labels: labels,
        chart: {
            type: 'donut',
            height: 300,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent'
        },
        colors: ['#00D26A', '#FF4757', '#3B82F6', '#8B5CF6', '#F59E0B'],
        dataLabels: {
            enabled: false
        },
        legend: {
            position: 'bottom',
            labels: {
                colors: '#8B9AB1'
            }
        },
        tooltip: {
            theme: 'dark'
        }
    };

    const chart = new ApexCharts(element, options);
    chart.render();
    return chart;
}

/**
 * Render a histogram chart
 */
function renderHistogramChart(elementId, data, title) {
    const element = document.getElementById(elementId);
    if (!element || !data || data.length === 0) return;

    // Create bins
    const min = Math.min(...data);
    const max = Math.max(...data);
    const binCount = 10;
    const binSize = (max - min) / binCount;
    
    const bins = new Array(binCount).fill(0);
    const labels = [];
    
    for (let i = 0; i < binCount; i++) {
        const binStart = min + (i * binSize);
        const binEnd = binStart + binSize;
        labels.push(`${binStart.toFixed(1)}-${binEnd.toFixed(1)}`);
    }
    
    data.forEach(value => {
        const binIndex = Math.min(Math.floor((value - min) / binSize), binCount - 1);
        bins[binIndex]++;
    });

    return renderBarChart(elementId, labels, bins, title, ['#3B82F6']);
}

/**
 * Update circular chart score
 */
function updateCircularChart(circleElement, valueElement, score) {
    if (circleElement) {
        const percentage = Math.min(Math.max(score, 0), 100);
        circleElement.setAttribute('stroke-dasharray', `${percentage}, 100`);
        
        // Update color based on score
        if (percentage >= 70) {
            circleElement.style.stroke = '#00D26A';
        } else if (percentage >= 50) {
            circleElement.style.stroke = '#F59E0B';
        } else {
            circleElement.style.stroke = '#FF4757';
        }
    }
    
    if (valueElement) {
        valueElement.textContent = Math.round(score);
    }
}

/**
 * Destroy chart instance
 */
function destroyChart(chart) {
    if (chart && typeof chart.destroy === 'function') {
        chart.destroy();
    }
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        renderAreaChart,
        renderBarChart,
        renderLineChart,
        renderDonutChart,
        renderHistogramChart,
        updateCircularChart,
        destroyChart
    };
}

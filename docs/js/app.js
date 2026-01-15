/**
 * FIGARO-NAM Explorer - Haupt-Anwendungslogik
 * Laedt Daten und initialisiert Visualisierungen
 */

// Globale Daten
let DATA = {
    timeSeries: null,
    trade: null,
    sectors: null,
    linkages: null,
    sankey: null,
    metadata: null
};

// Export for other modules
window.APP_DATA = DATA;

// Farben fuer Laender
const COUNTRY_COLORS = {
    'DE': '#3498db',
    'FR': '#e74c3c',
    'IT': '#27ae60',
    'ES': '#f39c12',
    'AT': '#9b59b6',
    'PL': '#1abc9c',
    'GR': '#e67e22',
    'NL': '#34495e'
};

/**
 * Daten laden
 */
async function loadData() {
    try {
        const [timeSeries, trade, sectors, linkages, sankey, metadata] = await Promise.all([
            d3.json('data/time_series.json'),
            d3.json('data/trade_partners.json'),
            d3.json('data/sectors.json'),
            d3.json('data/linkages.json'),
            d3.json('data/sankey.json').catch(() => null),
            d3.json('data/metadata.json')
        ]);

        DATA.timeSeries = timeSeries;
        DATA.trade = trade;
        DATA.sectors = sectors;
        DATA.linkages = linkages;
        DATA.sankey = sankey;
        DATA.metadata = metadata;

        // Update global reference
        window.APP_DATA = DATA;

        console.log('Daten geladen:', DATA);
        return true;
    } catch (error) {
        console.error('Fehler beim Laden der Daten:', error);
        return false;
    }
}

/**
 * Tab-Navigation
 */
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;

            // Aktiven Tab wechseln
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');

            // Chart neu zeichnen bei Tab-Wechsel
            switch(tabId) {
                case 'zeitreihen':
                    if (typeof updateTimeSeriesChart === 'function') updateTimeSeriesChart();
                    break;
                case 'erholung':
                    if (typeof updateRecoveryChart === 'function') updateRecoveryChart();
                    break;
                case 'kreislauf':
                    if (typeof updateSankeyChart === 'function') updateSankeyChart();
                    break;
                case 'handel':
                    if (typeof updateTradeChart === 'function') updateTradeChart();
                    break;
                case 'sektoren':
                    if (typeof updateSectorsChart === 'function') updateSectorsChart();
                    break;
                case 'verflechtung':
                    if (typeof updateLinkagesChart === 'function') updateLinkagesChart();
                    break;
            }
        });
    });
}

/**
 * Tooltip erstellen
 */
function createTooltip() {
    return d3.select('body')
        .append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0);
}

/**
 * Tooltip anzeigen
 */
function showTooltip(tooltip, html, event) {
    tooltip.transition()
        .duration(200)
        .style('opacity', 1);
    tooltip.html(html)
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px');
}

/**
 * Tooltip verstecken
 */
function hideTooltip(tooltip) {
    tooltip.transition()
        .duration(500)
        .style('opacity', 0);
}

/**
 * Zahl formatieren
 */
function formatNumber(num, decimals = 1) {
    if (num === null || num === undefined || isNaN(num)) return '-';
    if (Math.abs(num) >= 1e9) {
        return (num / 1e9).toFixed(decimals) + ' Mrd.';
    } else if (Math.abs(num) >= 1e6) {
        return (num / 1e6).toFixed(decimals) + ' Mio.';
    } else if (Math.abs(num) >= 1e3) {
        return (num / 1e3).toFixed(decimals) + ' Tsd.';
    }
    return num.toFixed(decimals);
}

/**
 * Prozent formatieren
 */
function formatPercent(num, decimals = 1) {
    if (num === null || num === undefined || isNaN(num)) return '-';
    const sign = num >= 0 ? '+' : '';
    return sign + num.toFixed(decimals) + '%';
}

/**
 * Initialisierung
 */
async function init() {
    console.log('FIGARO-NAM Explorer wird initialisiert...');

    // Daten laden
    const loaded = await loadData();
    if (!loaded) {
        alert('Fehler beim Laden der Daten. Bitte Seite neu laden.');
        return;
    }

    // Tab-Navigation initialisieren
    initTabs();

    // Visualisierungen initialisieren
    if (typeof initTimeSeriesChart === 'function') initTimeSeriesChart();
    if (typeof initRecoveryChart === 'function') initRecoveryChart();
    if (typeof initSankeyChart === 'function') initSankeyChart();
    if (typeof initTradeChart === 'function') initTradeChart();
    if (typeof initSectorsChart === 'function') initSectorsChart();
    if (typeof initLinkagesChart === 'function') initLinkagesChart();

    console.log('Initialisierung abgeschlossen.');
}

/**
 * Format value in millions
 */
function formatMio(value) {
    if (value === null || value === undefined || isNaN(value)) return '-';
    if (Math.abs(value) >= 1e6) {
        return (value / 1e6).toFixed(1) + ' Bio. EUR';
    } else if (Math.abs(value) >= 1e3) {
        return (value / 1e3).toFixed(1) + ' Mrd. EUR';
    }
    return value.toFixed(1) + ' Mio. EUR';
}

// Export formatting function
window.formatMio = formatMio;

// Start
document.addEventListener('DOMContentLoaded', init);

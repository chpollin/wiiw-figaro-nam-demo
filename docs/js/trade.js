/**
 * FIGARO-NAM Explorer - Trade Partners Visualization
 * Horizontal bar chart for exports/imports/balance
 *
 * Multi-country support: Data structure is {country: {data}}
 */

let tradeTooltip = null;
let tradeMode = 'exports';
let tradeTopN = 15;
let tradeCountry = 'DE';

// Focus countries
const TRADE_FOCUS_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'AT', 'PL', 'GR', 'NL'];
const TRADE_COUNTRY_NAMES = {
    'DE': 'Germany',
    'FR': 'France',
    'IT': 'Italy',
    'ES': 'Spain',
    'AT': 'Austria',
    'PL': 'Poland',
    'GR': 'Greece',
    'NL': 'Netherlands'
};

/**
 * Populate country dropdown for trade
 */
function populateTradeCountryDropdown() {
    const countrySelect = document.getElementById('trade-country');
    if (!countrySelect) return;

    // Clear existing options
    countrySelect.innerHTML = '';

    // Get available countries from data
    const tradeData = DATA && DATA.trade;
    const availableCountries = tradeData ? Object.keys(tradeData).filter(k => k !== '_meta' && k !== 'country') : TRADE_FOCUS_COUNTRIES;

    // Add options for each country
    TRADE_FOCUS_COUNTRIES.forEach(ctr => {
        const option = document.createElement('option');
        option.value = ctr;
        option.textContent = TRADE_COUNTRY_NAMES[ctr] || ctr;
        option.disabled = !availableCountries.includes(ctr);
        if (ctr === tradeCountry) option.selected = true;
        countrySelect.appendChild(option);
    });
}

/**
 * Initialize trade chart
 */
function initTradeChart() {
    if (!DATA.trade) return;

    // Populate country dropdown
    populateTradeCountryDropdown();

    // Create tooltip
    tradeTooltip = createTooltip();

    // Country dropdown
    const countrySelect = document.getElementById('trade-country');
    if (countrySelect) {
        countrySelect.addEventListener('change', () => {
            tradeCountry = countrySelect.value;
            updateTradeChart();
        });
    }

    // Mode dropdown
    const modeSelect = document.getElementById('trade-mode');
    if (modeSelect) {
        modeSelect.addEventListener('change', () => {
            tradeMode = modeSelect.value;
            updateTopNLabel();
            updateTradeChart();
        });
    }

    // TopN slider
    const topnSlider = document.getElementById('trade-topn');
    const topnValue = document.getElementById('trade-topn-value');
    if (topnSlider) {
        topnSlider.addEventListener('input', () => {
            tradeTopN = parseInt(topnSlider.value);
            if (topnValue) topnValue.textContent = tradeTopN;
            updateTradeChart();
        });
    }

    // Draw chart
    updateTradeChart();
}

/**
 * Get country-specific trade data
 */
function getTradeCountryData() {
    if (!DATA.trade) return null;

    // New structure: {country: {data}}
    let countryData = DATA.trade[tradeCountry];

    // Fallback to DE if country not available
    if (!countryData && DATA.trade['DE']) {
        countryData = DATA.trade['DE'];
        console.log(`Trade: Using Germany data as fallback for ${tradeCountry}`);
    }

    // Handle old structure (direct data without country key)
    if (!countryData && DATA.trade.exports) {
        countryData = DATA.trade;
    }

    return countryData;
}

/**
 * Update trade chart
 */
function updateTradeChart() {
    if (!DATA.trade) return;

    const svg = d3.select('#chart-handel');
    svg.selectAll('*').remove();

    const container = document.querySelector('#chart-handel').parentElement;
    const margin = { top: 30, right: 40, bottom: 50, left: 120 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Abort if container not visible (tab inactive)
    if (width <= 0 || height <= 0) return;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Get country-specific data
    const countryData = getTradeCountryData();
    if (!countryData) {
        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .text('No data available for ' + (TRADE_COUNTRY_NAMES[tradeCountry] || tradeCountry));
        return;
    }

    const countryName = TRADE_COUNTRY_NAMES[tradeCountry] || tradeCountry;
    const year = countryData.year || 2019;

    // Data based on mode
    let data = [];
    let title = '';

    if (tradeMode === 'exports') {
        data = countryData.exports ? countryData.exports.slice(0, tradeTopN) : [];
        title = `Exports by Trade Partner (${countryName} ${year})`;
    } else if (tradeMode === 'imports') {
        data = countryData.imports ? countryData.imports.slice(0, tradeTopN) : [];
        title = `Imports by Trade Partner (${countryName} ${year})`;
    } else if (tradeMode === 'balance') {
        data = countryData.balance ? countryData.balance.slice(0, tradeTopN) : [];
        title = `Trade Balance by Partner (${countryName} ${year})`;
    } else if (tradeMode === 'sectors') {
        data = countryData.imports_by_sector ? countryData.imports_by_sector.slice(0, tradeTopN) : [];
        title = `Imports by Product Group - Import Intensity (${countryName} ${year})`;
    }

    if (data.length === 0) {
        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .text('No data available');
        return;
    }

    // Title
    g.append('text')
        .attr('x', width / 2)
        .attr('y', -10)
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', '600')
        .text(title);

    if (tradeMode === 'balance') {
        drawBalanceChart(g, data, width, height);
    } else if (tradeMode === 'sectors') {
        drawSectorImportsChart(g, data, width, height);
    } else {
        drawBarChart(g, data, width, height, tradeMode);
    }
}

/**
 * Simple bar chart (export or import)
 */
function drawBarChart(g, data, width, height, mode) {
    const valueKey = 'value';
    const barClass = mode === 'exports' ? 'bar-export' : 'bar-import';

    // Scales
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.partner_name))
        .range([0, height])
        .padding(0.2);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d[valueKey]) * 1.1])
        .range([0, width]);

    // Axes
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale));

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => formatNumber(d, 0)));

    // X-axis label
    g.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#7f8c8d')
        .text('million EUR');

    // Bars
    g.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', barClass)
        .attr('y', d => yScale(d.partner_name))
        .attr('x', 0)
        .attr('height', yScale.bandwidth())
        .attr('width', d => xScale(d[valueKey]))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(tradeTooltip,
                `<strong>${d.partner_name}</strong><br/>
                 Value: ${formatNumber(d[valueKey])} EUR<br/>
                 Share: ${d.share.toFixed(1)}%`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(tradeTooltip);
        });

    // Values on bars
    g.selectAll('.bar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.partner_name) + yScale.bandwidth() / 2 + 4)
        .attr('x', d => xScale(d[valueKey]) + 5)
        .style('font-size', '10px')
        .style('fill', '#7f8c8d')
        .text(d => d.share.toFixed(1) + '%');
}

/**
 * Trade balance chart (export vs import with net)
 */
function drawBalanceChart(g, data, width, height) {
    // Scales
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.partner_name))
        .range([0, height])
        .padding(0.2);

    const maxVal = d3.max(data, d => Math.max(d.exports, d.imports));
    const xScale = d3.scaleLinear()
        .domain([0, maxVal * 1.1])
        .range([0, width / 2 - 20]);

    // Center line
    const center = width / 2;

    g.append('line')
        .attr('x1', center)
        .attr('x2', center)
        .attr('y1', 0)
        .attr('y2', height)
        .style('stroke', '#bdc3c7')
        .style('stroke-width', 1);

    // Y-axis (partner names)
    g.append('g')
        .attr('class', 'axis y-axis')
        .attr('transform', `translate(${center},0)`)
        .call(d3.axisLeft(yScale).tickSize(0))
        .selectAll('text')
        .style('text-anchor', 'middle');

    // Export bars (right)
    g.selectAll('.bar-export')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar-export')
        .attr('y', d => yScale(d.partner_name))
        .attr('x', center + 5)
        .attr('height', yScale.bandwidth() / 2)
        .attr('width', d => xScale(d.exports))
        .on('mouseover', function(event, d) {
            showTooltip(tradeTooltip,
                `<strong>${d.partner_name}</strong><br/>
                 Exports: ${formatNumber(d.exports)} EUR<br/>
                 Imports: ${formatNumber(d.imports)} EUR<br/>
                 Net: ${formatNumber(d.net)} EUR`,
                event);
        })
        .on('mouseout', function() {
            hideTooltip(tradeTooltip);
        });

    // Import bars (left, mirrored)
    g.selectAll('.bar-import')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar-import')
        .attr('y', d => yScale(d.partner_name) + yScale.bandwidth() / 2)
        .attr('x', d => center - 5 - xScale(d.imports))
        .attr('height', yScale.bandwidth() / 2)
        .attr('width', d => xScale(d.imports))
        .on('mouseover', function(event, d) {
            showTooltip(tradeTooltip,
                `<strong>${d.partner_name}</strong><br/>
                 Exports: ${formatNumber(d.exports)} EUR<br/>
                 Imports: ${formatNumber(d.imports)} EUR<br/>
                 Net: ${formatNumber(d.net)} EUR`,
                event);
        })
        .on('mouseout', function() {
            hideTooltip(tradeTooltip);
        });

    // Legend
    const legend = g.append('g')
        .attr('transform', `translate(${width - 100}, -20)`);

    legend.append('rect')
        .attr('width', 12)
        .attr('height', 12)
        .attr('fill', '#27ae60');
    legend.append('text')
        .attr('x', 16)
        .attr('y', 10)
        .style('font-size', '11px')
        .text('Exports');

    legend.append('rect')
        .attr('x', 70)
        .attr('width', 12)
        .attr('height', 12)
        .attr('fill', '#e74c3c');
    legend.append('text')
        .attr('x', 86)
        .attr('y', 10)
        .style('font-size', '11px')
        .text('Imports');
}

/**
 * Sector imports chart (import intensity)
 */
function drawSectorImportsChart(g, data, width, height) {
    // Scales
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.label || d.code))
        .range([0, height])
        .padding(0.2);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value) * 1.1])
        .range([0, width]);

    // Axes
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale));

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => formatNumber(d, 0)));

    // X-axis label
    g.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#7f8c8d')
        .text('million EUR (Imports)');

    // Bars
    g.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar-import')
        .attr('y', d => yScale(d.label || d.code))
        .attr('x', 0)
        .attr('height', yScale.bandwidth())
        .attr('width', d => xScale(d.value))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(tradeTooltip,
                `<strong>${d.label || d.code}</strong><br/>
                 Code: ${d.code}<br/>
                 Imports: ${formatNumber(d.value)} EUR<br/>
                 Share: ${d.share ? d.share.toFixed(1) + '%' : '-'}`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(tradeTooltip);
        });

    // Values on bars
    g.selectAll('.bar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.label || d.code) + yScale.bandwidth() / 2 + 4)
        .attr('x', d => xScale(d.value) + 5)
        .style('font-size', '10px')
        .style('fill', '#7f8c8d')
        .text(d => d.share ? d.share.toFixed(1) + '%' : '');
}

/**
 * Update label for TopN slider based on mode
 */
function updateTopNLabel() {
    const label = document.getElementById('trade-topn-label');
    if (label) {
        if (tradeMode === 'sectors') {
            label.textContent = 'Number of Sectors';
        } else {
            label.textContent = 'Number of Partners';
        }
    }
}

// Window resize
window.addEventListener('resize', () => {
    if (document.getElementById('trade').classList.contains('active')) {
        updateTradeChart();
    }
});

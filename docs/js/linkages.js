/**
 * FIGARO-NAM Explorer - IO Linkages Visualization
 * Bar chart for backward/forward linkages
 *
 * Multi-country support: Data structure is {country: {data}}
 */

let linkagesTooltip = null;
let linkageMode = 'backward';
let linkagesCountry = 'DE';

// Focus countries
const LINKAGES_FOCUS_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'AT', 'PL', 'GR', 'NL'];
const LINKAGES_COUNTRY_NAMES = {
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
 * Populate country dropdown for linkages
 */
function populateLinkagesCountryDropdown() {
    const countrySelect = document.getElementById('linkages-country');
    if (!countrySelect) return;

    // Clear existing options
    countrySelect.innerHTML = '';

    // Get available countries from data
    const linkagesData = DATA && DATA.linkages;
    const availableCountries = linkagesData ? Object.keys(linkagesData).filter(k => k !== '_meta' && k !== 'country') : LINKAGES_FOCUS_COUNTRIES;

    // Add options for each country
    LINKAGES_FOCUS_COUNTRIES.forEach(ctr => {
        const option = document.createElement('option');
        option.value = ctr;
        option.textContent = LINKAGES_COUNTRY_NAMES[ctr] || ctr;
        option.disabled = !availableCountries.includes(ctr);
        if (ctr === linkagesCountry) option.selected = true;
        countrySelect.appendChild(option);
    });
}

/**
 * Get country-specific linkages data
 */
function getLinkagesCountryData() {
    if (!DATA.linkages) return null;

    // New structure: {country: {data}}
    let countryData = DATA.linkages[linkagesCountry];

    // Fallback to DE if country not available
    if (!countryData && DATA.linkages['DE']) {
        countryData = DATA.linkages['DE'];
        console.log(`Linkages: Using Germany data as fallback for ${linkagesCountry}`);
    }

    // Handle old structure (direct data without country key)
    if (!countryData && DATA.linkages.backward) {
        countryData = DATA.linkages;
    }

    return countryData;
}

/**
 * Initialize linkages chart
 */
function initLinkagesChart() {
    if (!DATA.linkages) return;

    // Populate country dropdown
    populateLinkagesCountryDropdown();

    // Create tooltip
    linkagesTooltip = createTooltip();

    // Country dropdown
    const countrySelect = document.getElementById('linkages-country');
    if (countrySelect) {
        countrySelect.addEventListener('change', () => {
            linkagesCountry = countrySelect.value;
            updateLinkagesChart();
        });
    }

    // Mode dropdown
    const modeSelect = document.getElementById('linkage-mode');
    if (modeSelect) {
        modeSelect.addEventListener('change', () => {
            linkageMode = modeSelect.value;
            updateLinkagesChart();
        });
    }

    // Draw chart
    updateLinkagesChart();
}

/**
 * Update linkages chart
 */
function updateLinkagesChart() {
    const countryData = getLinkagesCountryData();
    if (!countryData) return;

    const svg = d3.select('#chart-verflechtung');
    svg.selectAll('*').remove();

    const container = document.querySelector('#chart-verflechtung').parentElement;
    const margin = { top: 40, right: 60, bottom: 50, left: 220 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Abort if container not visible (tab inactive)
    if (width <= 0 || height <= 0) return;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const countryName = LINKAGES_COUNTRY_NAMES[linkagesCountry] || linkagesCountry;
    const year = countryData.year || 2019;

    // Data based on mode
    let data = [];
    let title = '';
    let xLabel = '';

    if (linkageMode === 'backward') {
        data = countryData.backward || [];
        title = `Backward Linkages: Which industries purchase the most intermediate inputs? (${countryName} ${year})`;
        xLabel = 'Intermediate Inputs (million EUR)';
    } else if (linkageMode === 'forward') {
        data = countryData.forward || [];
        title = `Forward Linkages: Which products supply the most to other sectors? (${countryName} ${year})`;
        xLabel = 'Total Supply (million EUR)';
    } else if (linkageMode === 'flows') {
        data = countryData.top_flows || [];
        title = `Top Intersectoral Flows (${countryName} ${year})`;
        xLabel = 'Flow (million EUR)';
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
        .attr('y', -20)
        .attr('text-anchor', 'middle')
        .style('font-size', '13px')
        .style('font-weight', '600')
        .text(title);

    if (linkageMode === 'flows') {
        drawFlowsChart(g, data, width, height, xLabel);
    } else {
        drawLinkageBarChart(g, data, width, height, xLabel);
    }
}

/**
 * Bar chart for linkages
 */
function drawLinkageBarChart(g, data, width, height, xLabel) {
    // Scales
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, height])
        .padding(0.15);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value) * 1.1])
        .range([0, width]);

    // Axes
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale))
        .selectAll('text')
        .style('font-size', '10px');

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => formatNumber(d, 0)));

    // X-axis label
    g.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '11px')
        .style('fill', '#7f8c8d')
        .text(xLabel);

    // Bars
    g.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar-neutral')
        .attr('y', d => yScale(d.label))
        .attr('x', 0)
        .attr('height', yScale.bandwidth())
        .attr('width', d => xScale(d.value))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(linkagesTooltip,
                `<strong>${d.label}</strong><br/>
                 Code: ${d.code}<br/>
                 Value: ${formatNumber(d.value)} EUR`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(linkagesTooltip);
        });

    // Values on bars
    g.selectAll('.bar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.label) + yScale.bandwidth() / 2 + 3)
        .attr('x', d => xScale(d.value) + 5)
        .style('font-size', '9px')
        .style('fill', '#7f8c8d')
        .text(d => formatNumber(d.value, 0));
}

/**
 * Chart for intersectoral flows
 */
function drawFlowsChart(g, data, width, height, xLabel) {
    // Create labels: "From -> To"
    const labeledData = data.map(d => ({
        ...d,
        displayLabel: `${d.from_label} -> ${d.to_label}`
    }));

    // Scales
    const yScale = d3.scaleBand()
        .domain(labeledData.map(d => d.displayLabel))
        .range([0, height])
        .padding(0.15);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(labeledData, d => d.value) * 1.1])
        .range([0, width]);

    // Axes
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale))
        .selectAll('text')
        .style('font-size', '9px');

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => formatNumber(d, 0)));

    // X-axis label
    g.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .style('font-size', '11px')
        .style('fill', '#7f8c8d')
        .text(xLabel);

    // Color scale for flows
    const colorScale = d3.scaleSequential(d3.interpolateBlues)
        .domain([0, d3.max(labeledData, d => d.value)]);

    // Bars
    g.selectAll('.bar')
        .data(labeledData)
        .enter()
        .append('rect')
        .attr('y', d => yScale(d.displayLabel))
        .attr('x', 0)
        .attr('height', yScale.bandwidth())
        .attr('width', d => xScale(d.value))
        .attr('fill', d => colorScale(d.value))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(linkagesTooltip,
                `<strong>Intersectoral Flow</strong><br/>
                 From: ${d.from_label} (${d.from_code})<br/>
                 To: ${d.to_label} (${d.to_code})<br/>
                 Value: ${formatNumber(d.value)} EUR`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(linkagesTooltip);
        });

    // Values on bars
    g.selectAll('.bar-label')
        .data(labeledData)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.displayLabel) + yScale.bandwidth() / 2 + 3)
        .attr('x', d => xScale(d.value) + 5)
        .style('font-size', '9px')
        .style('fill', '#7f8c8d')
        .text(d => formatNumber(d.value, 1));
}

// Window resize
window.addEventListener('resize', () => {
    if (document.getElementById('linkages').classList.contains('active')) {
        updateLinkagesChart();
    }
});

/**
 * FIGARO-NAM Explorer - Time Series Visualization
 * Multi-Line Chart with Crisis Markers
 */

let tsChart = null;
let tsTooltip = null;
let selectedCountries = ['DE'];
let selectedAggregate = 'hh_consumption';

/**
 * Initialize country checkboxes
 */
function initCountryCheckboxes() {
    const container = document.getElementById('ts-laender');
    if (!container || !DATA.timeSeries) return;

    container.innerHTML = '';

    // Only show countries with data
    const aggregateData = DATA.timeSeries.aggregates['hh_consumption'] || {};
    const countriesWithData = DATA.timeSeries.countries.filter(code =>
        aggregateData[code] && aggregateData[code].length > 0
    );

    countriesWithData.forEach(code => {
        const label = document.createElement('label');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = code;
        checkbox.checked = code === 'DE';
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                if (!selectedCountries.includes(code)) {
                    selectedCountries.push(code);
                }
            } else {
                selectedCountries = selectedCountries.filter(c => c !== code);
            }
            updateTimeSeriesChart();
        });

        const name = DATA.timeSeries.country_names[code] || code;
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(name));
        container.appendChild(label);
    });

    // Note if only one country available
    if (countriesWithData.length === 1) {
        const hint = document.createElement('span');
        hint.className = 'data-hint';
        hint.textContent = ' (only DE data available)';
        hint.style.fontSize = '0.8em';
        hint.style.color = '#7f8c8d';
        container.appendChild(hint);
    }
}

/**
 * Initialize time series chart
 */
function initTimeSeriesChart() {
    if (!DATA.timeSeries) return;

    // Create tooltip
    tsTooltip = createTooltip();

    // Country checkboxes
    initCountryCheckboxes();

    // Aggregate dropdown
    const aggregatSelect = document.getElementById('ts-aggregat');
    if (aggregatSelect) {
        aggregatSelect.addEventListener('change', () => {
            selectedAggregate = aggregatSelect.value;
            updateTimeSeriesChart();
        });
    }

    // Draw chart
    updateTimeSeriesChart();
}

/**
 * Update time series chart
 */
function updateTimeSeriesChart() {
    if (!DATA.timeSeries) return;

    const svg = d3.select('#chart-zeitreihen');
    svg.selectAll('*').remove();

    const container = document.querySelector('#chart-zeitreihen').parentElement;
    const margin = { top: 30, right: 100, bottom: 50, left: 80 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Abort if container not visible
    if (width <= 0 || height <= 0) return;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Prepare data
    const years = DATA.timeSeries.years;
    const aggregateData = DATA.timeSeries.aggregates[selectedAggregate];

    if (!aggregateData) {
        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .text('No data available');
        return;
    }

    // Only countries with data and selected
    const validCountries = selectedCountries.filter(c => aggregateData[c] && aggregateData[c].length > 0);

    if (validCountries.length === 0) {
        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .text('Please select at least one country');
        return;
    }

    // Scales
    const xScale = d3.scaleLinear()
        .domain([d3.min(years), d3.max(years)])
        .range([0, width]);

    let allValues = [];
    validCountries.forEach(c => {
        if (aggregateData[c]) {
            allValues = allValues.concat(aggregateData[c]);
        }
    });

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(allValues) * 1.1])
        .range([height, 0]);

    // Axes
    const xAxis = d3.axisBottom(xScale)
        .tickFormat(d3.format('d'))
        .ticks(years.length);

    const yAxis = d3.axisLeft(yScale)
        .tickFormat(d => formatNumber(d, 0));

    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(xAxis);

    g.append('g')
        .attr('class', 'axis y-axis')
        .call(yAxis);

    // Y-axis label
    g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', -60)
        .attr('x', -height / 2)
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .style('fill', '#7f8c8d')
        .text('million EUR');

    // Crisis markers
    if (DATA.timeSeries.crisis_markers) {
        DATA.timeSeries.crisis_markers.forEach(crisis => {
            const x = xScale(crisis.year);

            g.append('line')
                .attr('class', 'crisis-marker')
                .attr('x1', x)
                .attr('x2', x)
                .attr('y1', 0)
                .attr('y2', height);

            g.append('text')
                .attr('class', 'crisis-label')
                .attr('x', x + 5)
                .attr('y', 15)
                .text(crisis.label);
        });
    }

    // Draw lines
    const line = d3.line()
        .x((d, i) => xScale(years[i]))
        .y(d => yScale(d))
        .curve(d3.curveMonotoneX);

    validCountries.forEach(country => {
        const values = aggregateData[country];
        if (!values || values.length === 0) return;

        g.append('path')
            .datum(values)
            .attr('class', `line line-${country}`)
            .attr('d', line)
            .style('stroke', COUNTRY_COLORS[country] || '#333');

        // Points for interaction
        g.selectAll(`.dot-${country}`)
            .data(values)
            .enter()
            .append('circle')
            .attr('class', `dot-${country}`)
            .attr('cx', (d, i) => xScale(years[i]))
            .attr('cy', d => yScale(d))
            .attr('r', 4)
            .style('fill', COUNTRY_COLORS[country] || '#333')
            .style('opacity', 0)
            .on('mouseover', function(event, d) {
                const i = values.indexOf(d);
                d3.select(this).style('opacity', 1);
                showTooltip(tsTooltip,
                    `<strong>${DATA.timeSeries.country_names[country]}</strong><br/>
                     ${years[i]}: ${formatNumber(d)} EUR`,
                    event);
            })
            .on('mouseout', function() {
                d3.select(this).style('opacity', 0);
                hideTooltip(tsTooltip);
            });
    });

    // Legend
    const legend = g.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width + 10}, 0)`);

    validCountries.forEach((country, i) => {
        const legendItem = legend.append('g')
            .attr('transform', `translate(0, ${i * 20})`);

        legendItem.append('line')
            .attr('x1', 0)
            .attr('x2', 20)
            .attr('y1', 0)
            .attr('y2', 0)
            .style('stroke', COUNTRY_COLORS[country] || '#333')
            .style('stroke-width', 2);

        legendItem.append('text')
            .attr('x', 25)
            .attr('y', 4)
            .style('font-size', '11px')
            .text(DATA.timeSeries.country_names[country] || country);
    });
}

// Window resize
window.addEventListener('resize', () => {
    if (document.getElementById('timeseries').classList.contains('active')) {
        updateTimeSeriesChart();
    }
});

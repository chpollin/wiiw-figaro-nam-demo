/**
 * FIGARO-NAM Explorer - Sector Dynamics
 * Diverging bar chart for YoY changes
 *
 * Multi-country support: Data structure is {country: {data}}
 */

let sectorsTooltip = null;
let selectedYear = '2020';
let sectorSort = 'change';
let sectorsCountry = 'DE';

// Focus countries
const SECTORS_FOCUS_COUNTRIES = ['DE', 'FR', 'IT', 'ES', 'AT', 'PL', 'GR', 'NL'];
const SECTORS_COUNTRY_NAMES = {
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
 * Populate country dropdown for sectors
 */
function populateSectorsCountryDropdown() {
    const countrySelect = document.getElementById('sectors-country');
    if (!countrySelect) return;

    // Clear existing options
    countrySelect.innerHTML = '';

    // Get available countries from data
    const sectorsData = DATA && DATA.sectors;
    const availableCountries = sectorsData ? Object.keys(sectorsData).filter(k => k !== '_meta' && k !== 'country') : SECTORS_FOCUS_COUNTRIES;

    // Add options for each country
    SECTORS_FOCUS_COUNTRIES.forEach(ctr => {
        const option = document.createElement('option');
        option.value = ctr;
        option.textContent = SECTORS_COUNTRY_NAMES[ctr] || ctr;
        option.disabled = !availableCountries.includes(ctr);
        if (ctr === sectorsCountry) option.selected = true;
        countrySelect.appendChild(option);
    });
}

/**
 * Get country-specific sectors data
 */
function getSectorsCountryData() {
    if (!DATA.sectors) return null;

    // New structure: {country: {data}}
    let countryData = DATA.sectors[sectorsCountry];

    // Fallback to DE if country not available
    if (!countryData && DATA.sectors['DE']) {
        countryData = DATA.sectors['DE'];
        console.log(`Sectors: Using Germany data as fallback for ${sectorsCountry}`);
    }

    // Handle old structure (direct data without country key)
    if (!countryData && DATA.sectors.dynamics) {
        countryData = DATA.sectors;
    }

    return countryData;
}

/**
 * Initialize sectors chart
 */
function initSectorsChart() {
    if (!DATA.sectors) return;

    // Populate country dropdown
    populateSectorsCountryDropdown();

    // Create tooltip
    sectorsTooltip = createTooltip();

    // Country dropdown
    const countrySelect = document.getElementById('sectors-country');
    if (countrySelect) {
        countrySelect.addEventListener('change', () => {
            sectorsCountry = countrySelect.value;
            updateSectorsChart();
        });
    }

    // Year buttons
    const yearBtns = document.querySelectorAll('.year-btn');
    yearBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            yearBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedYear = btn.dataset.year;
            updateSectorsChart();
        });
    });

    // Sort selection
    const sortSelect = document.getElementById('sector-sort');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            sectorSort = sortSelect.value;
            updateSectorsChart();
        });
    }

    // Draw chart
    updateSectorsChart();
}

/**
 * Update sectors chart
 */
function updateSectorsChart() {
    const countryData = getSectorsCountryData();
    if (!countryData || !countryData.dynamics) return;

    const svg = d3.select('#chart-sektoren');
    svg.selectAll('*').remove();

    const container = document.querySelector('#chart-sektoren').parentElement;
    const margin = { top: 40, right: 60, bottom: 30, left: 200 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Abort if container not visible (tab inactive)
    if (width <= 0 || height <= 0) return;

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Prepare data - change for selected year
    const changeKey = `change_${selectedYear}`;
    let data = countryData.dynamics
        .filter(d => d.code && d.code !== '' && !d.code.startsWith('B8'))  // No balance items
        .map(d => ({
            code: d.code,
            label: d.label,
            change: d[changeKey] || 0
        }))
        .filter(d => !isNaN(d.change));

    // Sort
    if (sectorSort === 'change') {
        data.sort((a, b) => a.change - b.change);
    } else {
        data.sort((a, b) => a.label.localeCompare(b.label));
    }

    // Limit to top/bottom 30 for readability
    if (data.length > 40) {
        const top20 = data.slice(-20);
        const bottom20 = data.slice(0, 20);
        data = [...bottom20, ...top20];
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
    const titleYear = selectedYear === '2020' ? '2019-2020 (COVID)' :
                      selectedYear === '2021' ? '2020-2021 (Recovery)' :
                      '2021-2022 (Energy Crisis)';
    const countryName = SECTORS_COUNTRY_NAMES[sectorsCountry] || sectorsCountry;
    g.append('text')
        .attr('x', width / 2)
        .attr('y', -20)
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', '600')
        .text(`Sector Change ${titleYear} (${countryName}, YoY %)`);

    // Scales
    const yScale = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, height])
        .padding(0.15);

    const maxAbs = d3.max(data, d => Math.abs(d.change));
    const xScale = d3.scaleLinear()
        .domain([-maxAbs * 1.1, maxAbs * 1.1])
        .range([0, width]);

    // Zero line
    const zeroX = xScale(0);

    g.append('line')
        .attr('x1', zeroX)
        .attr('x2', zeroX)
        .attr('y1', 0)
        .attr('y2', height)
        .style('stroke', '#2c3e50')
        .style('stroke-width', 1);

    // Y-axis
    g.append('g')
        .attr('class', 'axis y-axis')
        .call(d3.axisLeft(yScale))
        .selectAll('text')
        .style('font-size', '10px');

    // X-axis
    g.append('g')
        .attr('class', 'axis x-axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).tickFormat(d => d.toFixed(0) + '%'));

    // Bars
    g.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', d => d.change >= 0 ? 'bar-positive' : 'bar-negative')
        .attr('y', d => yScale(d.label))
        .attr('height', yScale.bandwidth())
        .attr('x', d => d.change >= 0 ? zeroX : xScale(d.change))
        .attr('width', d => Math.abs(xScale(d.change) - zeroX))
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.8);
            showTooltip(sectorsTooltip,
                `<strong>${d.label}</strong><br/>
                 Code: ${d.code}<br/>
                 Change: ${formatPercent(d.change)}`,
                event);
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 1);
            hideTooltip(sectorsTooltip);
        });

    // Values on bars
    g.selectAll('.bar-label')
        .data(data)
        .enter()
        .append('text')
        .attr('class', 'bar-label')
        .attr('y', d => yScale(d.label) + yScale.bandwidth() / 2 + 3)
        .attr('x', d => {
            if (d.change >= 0) {
                return xScale(d.change) + 3;
            } else {
                return xScale(d.change) - 3;
            }
        })
        .attr('text-anchor', d => d.change >= 0 ? 'start' : 'end')
        .style('font-size', '9px')
        .style('fill', '#7f8c8d')
        .text(d => formatPercent(d.change, 1));
}

// Window resize
window.addEventListener('resize', () => {
    if (document.getElementById('sectors').classList.contains('active')) {
        updateSectorsChart();
    }
});

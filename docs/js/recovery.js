/**
 * Recovery Chart - Vergleich mit Pre-COVID Niveau (2019)
 * Forschungsfrage B3: Hat die Energiekrise 2022 die COVID-Erholung gebremst?
 */

(function() {
    'use strict';

    let svg, g, width, height;
    const margin = { top: 40, right: 30, bottom: 100, left: 80 };

    // Country colors (same as timeseries)
    const countryColors = {
        'DE': '#3498db',
        'FR': '#e74c3c',
        'IT': '#27ae60',
        'ES': '#f39c12',
        'AT': '#9b59b6',
        'PL': '#1abc9c',
        'GR': '#e67e22',
        'NL': '#34495e'
    };

    const countryNames = {
        'DE': 'Deutschland',
        'FR': 'Frankreich',
        'IT': 'Italien',
        'ES': 'Spanien',
        'AT': 'Oesterreich',
        'PL': 'Polen',
        'GR': 'Griechenland',
        'NL': 'Niederlande'
    };

    function initRecoveryChart() {
        svg = d3.select('#chart-erholung');
        const container = document.querySelector('#chart-erholung').parentElement;

        const rect = container.getBoundingClientRect();
        width = rect.width - margin.left - margin.right;
        height = rect.height - margin.top - margin.bottom;

        if (width <= 0 || height <= 0) return;

        svg.selectAll('*').remove();

        g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Add title
        svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', margin.left + width / 2)
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('font-weight', '600')
            .text('Erholung gegenueber Pre-COVID Niveau (2019 = 0%)');
    }

    function updateRecoveryChart() {
        if (!window.APP_DATA || !window.APP_DATA.timeSeries) return;

        const data = window.APP_DATA.timeSeries;
        const period = document.getElementById('recovery-period').value;
        const aggregat = document.getElementById('recovery-aggregat').value;

        // Parse period selection
        const [compareYear] = period.split('vs');
        const targetYear = parseInt(compareYear);
        const baseYear = 2019;

        // Calculate recovery for each country
        const recoveryData = [];
        const countries = data.laender || [];
        const aggregateData = data.aggregate && data.aggregate[aggregat];
        const years = data.jahre || [];

        if (!aggregateData) return;

        const baseYearIdx = years.indexOf(baseYear);
        const targetYearIdx = years.indexOf(targetYear);

        if (baseYearIdx === -1 || targetYearIdx === -1) return;

        countries.forEach(ctr => {
            const values = aggregateData[ctr];
            if (!values || values.length <= Math.max(baseYearIdx, targetYearIdx)) return;

            const baseValue = values[baseYearIdx];
            const targetValue = values[targetYearIdx];

            if (baseValue && baseValue > 0) {
                const recovery = ((targetValue - baseValue) / baseValue) * 100;
                recoveryData.push({
                    country: ctr,
                    name: countryNames[ctr] || ctr,
                    recovery: recovery,
                    baseValue: baseValue,
                    targetValue: targetValue
                });
            }
        });

        // Sort by recovery (ascending = worst first)
        recoveryData.sort((a, b) => a.recovery - b.recovery);

        // Redraw chart
        initRecoveryChart();
        if (width <= 0 || height <= 0) return;

        // X scale (countries)
        const x = d3.scaleBand()
            .domain(recoveryData.map(d => d.country))
            .range([0, width])
            .padding(0.3);

        // Y scale (recovery percentage)
        const maxAbs = Math.max(
            Math.abs(d3.min(recoveryData, d => d.recovery) || 0),
            Math.abs(d3.max(recoveryData, d => d.recovery) || 0),
            10
        );
        const y = d3.scaleLinear()
            .domain([-maxAbs * 1.1, maxAbs * 1.1])
            .range([height, 0]);

        // X axis
        g.append('g')
            .attr('class', 'axis x-axis')
            .attr('transform', `translate(0,${y(0)})`)
            .call(d3.axisBottom(x).tickFormat(d => countryNames[d] || d))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end');

        // Y axis
        g.append('g')
            .attr('class', 'axis y-axis')
            .call(d3.axisLeft(y).tickFormat(d => d + '%'));

        // Y axis label
        g.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', -60)
            .attr('x', -height / 2)
            .attr('text-anchor', 'middle')
            .style('font-size', '12px')
            .text('Veraenderung gegenueber 2019');

        // Zero baseline
        g.append('line')
            .attr('class', 'baseline-marker')
            .attr('x1', 0)
            .attr('x2', width)
            .attr('y1', y(0))
            .attr('y2', y(0));

        // Bars
        g.selectAll('.bar')
            .data(recoveryData)
            .enter()
            .append('rect')
            .attr('class', d => d.recovery >= 0 ? 'bar-recovery-positive' : 'bar-recovery-negative')
            .attr('x', d => x(d.country))
            .attr('width', x.bandwidth())
            .attr('y', d => d.recovery >= 0 ? y(d.recovery) : y(0))
            .attr('height', d => Math.abs(y(d.recovery) - y(0)))
            .attr('fill', d => countryColors[d.country])
            .attr('opacity', 0.85)
            .on('mouseover', function(event, d) {
                d3.select(this).attr('opacity', 1);
                showTooltip(event, d, aggregat, targetYear);
            })
            .on('mouseout', function() {
                d3.select(this).attr('opacity', 0.85);
                hideTooltip();
            });

        // Value labels on bars
        g.selectAll('.value-label')
            .data(recoveryData)
            .enter()
            .append('text')
            .attr('class', 'value-label')
            .attr('x', d => x(d.country) + x.bandwidth() / 2)
            .attr('y', d => d.recovery >= 0 ? y(d.recovery) - 5 : y(d.recovery) + 15)
            .attr('text-anchor', 'middle')
            .style('font-size', '11px')
            .style('font-weight', '600')
            .style('fill', d => d.recovery >= 0 ? '#27ae60' : '#e74c3c')
            .text(d => (d.recovery >= 0 ? '+' : '') + d.recovery.toFixed(1) + '%');
    }

    function showTooltip(event, d, aggregat, year) {
        const aggregatNames = {
            'hh_konsum': 'Privater Konsum',
            'staat_konsum': 'Staatskonsum',
            'investitionen': 'Investitionen'
        };

        const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');

        tooltip.html(`
            <strong>${d.name}</strong><br/>
            ${aggregatNames[aggregat] || aggregat}<br/>
            2019: ${window.formatMio(d.baseValue)}<br/>
            ${year}: ${window.formatMio(d.targetValue)}<br/>
            <strong>Veraenderung: ${(d.recovery >= 0 ? '+' : '') + d.recovery.toFixed(1)}%</strong>
        `);
    }

    function hideTooltip() {
        d3.selectAll('.tooltip').remove();
    }

    // Event listeners
    document.addEventListener('DOMContentLoaded', function() {
        const periodSelect = document.getElementById('recovery-period');
        const aggregatSelect = document.getElementById('recovery-aggregat');

        if (periodSelect) {
            periodSelect.addEventListener('change', updateRecoveryChart);
        }
        if (aggregatSelect) {
            aggregatSelect.addEventListener('change', updateRecoveryChart);
        }
    });

    // Export for app.js
    window.initRecoveryChart = initRecoveryChart;
    window.updateRecoveryChart = updateRecoveryChart;

})();

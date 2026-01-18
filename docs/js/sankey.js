/**
 * Sankey Diagram - Economic Circular Flow Visualization
 * Research Question A1: How does value added flow from production through income to final use?
 *
 * Flow: Production -> Income -> Final Use
 *       (Industries)  (D-Codes)  (P-Codes)
 */

(function() {
    'use strict';

    let svg, g, width, height;
    const margin = { top: 30, right: 150, bottom: 30, left: 30 };

    // Color palette for flow stages - distinct colors for better readability
    const stageColors = {
        production: '#2563eb',   // Production (Industries) - Blue
        income: '#059669',       // Income (D11, B2, B3) - Emerald Green
        distribution: '#7c3aed', // National Income (Distribution) - Purple
        use: '#dc2626'           // Final Use (P3, P51G, P6) - Red
    };

    function initSankeyChart() {
        svg = d3.select('#chart-kreislauf');
        const container = document.querySelector('#chart-kreislauf').parentElement;

        const rect = container.getBoundingClientRect();
        width = rect.width - margin.left - margin.right;
        height = rect.height - margin.top - margin.bottom;

        if (width <= 0 || height <= 0) return;

        svg.selectAll('*').remove();

        g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);
    }

    function updateSankeyChart() {
        if (!window.APP_DATA || !window.APP_DATA.sankey) {
            showPlaceholder();
            return;
        }

        const sankeyData = window.APP_DATA.sankey;
        const year = document.getElementById('sankey-year').value;

        const yearData = sankeyData[year];
        if (!yearData) {
            showPlaceholder();
            return;
        }

        initSankeyChart();
        if (width <= 0 || height <= 0) return;

        // Build nodes and links from data
        const { nodes, links } = buildSankeyGraph(yearData);

        // Create sankey generator
        const sankey = d3.sankey()
            .nodeId(d => d.name)
            .nodeWidth(20)
            .nodePadding(15)
            .extent([[0, 0], [width, height]]);

        // Generate layout
        const graph = sankey({
            nodes: nodes.map(d => Object.assign({}, d)),
            links: links.map(d => Object.assign({}, d))
        });

        // Draw links
        g.append('g')
            .attr('class', 'sankey-links')
            .selectAll('path')
            .data(graph.links)
            .enter()
            .append('path')
            .attr('class', 'sankey-link')
            .attr('d', d3.sankeyLinkHorizontal())
            .attr('stroke', d => getNodeColor(d.source.stage))
            .attr('stroke-width', d => Math.max(1, d.width))
            .on('mouseover', function(event, d) {
                d3.select(this).attr('stroke-opacity', 0.7);
                showLinkTooltip(event, d);
            })
            .on('mouseout', function() {
                d3.select(this).attr('stroke-opacity', 0.4);
                hideTooltip();
            });

        // Draw nodes
        const node = g.append('g')
            .attr('class', 'sankey-nodes')
            .selectAll('g')
            .data(graph.nodes)
            .enter()
            .append('g')
            .attr('class', 'sankey-node');

        node.append('rect')
            .attr('x', d => d.x0)
            .attr('y', d => d.y0)
            .attr('height', d => Math.max(1, d.y1 - d.y0))
            .attr('width', d => d.x1 - d.x0)
            .attr('fill', d => getNodeColor(d.stage))
            .on('mouseover', function(event, d) {
                showNodeTooltip(event, d);
            })
            .on('mouseout', hideTooltip);

        // Node labels
        node.append('text')
            .attr('x', d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
            .attr('y', d => (d.y1 + d.y0) / 2)
            .attr('dy', '0.35em')
            .attr('text-anchor', d => d.x0 < width / 2 ? 'start' : 'end')
            .text(d => d.label)
            .style('font-size', '11px');

        // Stage labels (top)
        const stageLabels = [
            { x: 0, label: 'Income' },
            { x: width / 2, label: 'Distribution' },
            { x: width, label: 'Final Use' }
        ];

        svg.selectAll('.stage-label')
            .data(stageLabels)
            .enter()
            .append('text')
            .attr('class', 'stage-label')
            .attr('x', d => margin.left + d.x)
            .attr('y', 15)
            .attr('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('font-weight', '600')
            .style('fill', '#7f8c8d')
            .text(d => d.label);
    }

    function buildSankeyGraph(data) {
        // Nodes: Income sources -> Final uses
        const nodes = [];
        const links = [];

        // Income sources (left)
        const incomeSources = [
            { name: 'D11', label: 'Wages (D11)', stage: 'income', value: data.D11 || 0 },
            { name: 'B2', label: 'Operating Surplus (B2)', stage: 'income', value: data.B2 || 0 },
            { name: 'B3', label: 'Mixed Income (B3)', stage: 'income', value: data.B3 || 0 }
        ];

        // Final uses (right)
        const finalUses = [
            { name: 'P3_S14', label: 'Household Consumption', stage: 'use', value: data.P3_S14 || 0 },
            { name: 'P3_S13', label: 'Government Consumption', stage: 'use', value: data.P3_S13 || 0 },
            { name: 'P51G', label: 'Investment', stage: 'use', value: data.P51G || 0 },
            { name: 'net_exports', label: 'Net Exports', stage: 'use', value: data.net_exports || 0 }
        ];

        // Intermediate node (distribution)
        const totalIncome = incomeSources.reduce((sum, d) => sum + d.value, 0);
        nodes.push({ name: 'NationalIncome', label: 'National Income', stage: 'distribution', value: totalIncome });

        // Add all nodes
        incomeSources.forEach(d => { if (d.value > 0) nodes.push(d); });
        finalUses.forEach(d => { if (d.value > 0) nodes.push(d); });

        // Links: Income -> Distribution
        incomeSources.forEach(source => {
            if (source.value > 0) {
                links.push({
                    source: source.name,
                    target: 'NationalIncome',
                    value: source.value
                });
            }
        });

        // Links: Distribution -> Final uses (proportional)
        const totalUse = finalUses.reduce((sum, d) => sum + Math.max(0, d.value), 0);
        finalUses.forEach(use => {
            if (use.value > 0) {
                // Scale to match total income
                const scaledValue = (use.value / totalUse) * totalIncome * 0.95;
                links.push({
                    source: 'NationalIncome',
                    target: use.name,
                    value: scaledValue
                });
            }
        });

        return { nodes, links };
    }

    function getNodeColor(stage) {
        return stageColors[stage] || '#95a5a6';
    }

    function showPlaceholder() {
        initSankeyChart();
        if (width <= 0 || height <= 0) return;

        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('text-anchor', 'middle')
            .style('font-size', '14px')
            .style('fill', '#7f8c8d')
            .text('Sankey data is being generated...');

        g.append('text')
            .attr('x', width / 2)
            .attr('y', height / 2 + 25)
            .attr('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('fill', '#95a5a6')
            .text('Please regenerate the JSON data.');
    }

    function showNodeTooltip(event, d) {
        const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');

        tooltip.html(`
            <strong>${d.label}</strong><br/>
            Value: ${window.formatMio ? window.formatMio(d.value) : d.value.toFixed(0) + ' m EUR'}
        `);
    }

    function showLinkTooltip(event, d) {
        const tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');

        tooltip.html(`
            <strong>${d.source.label} &rarr; ${d.target.label}</strong><br/>
            Flow: ${window.formatMio ? window.formatMio(d.value) : d.value.toFixed(0) + ' m EUR'}
        `);
    }

    function hideTooltip() {
        d3.selectAll('.tooltip').remove();
    }

    // Event listeners
    document.addEventListener('DOMContentLoaded', function() {
        const yearSelect = document.getElementById('sankey-year');
        const countrySelect = document.getElementById('sankey-country');

        if (yearSelect) {
            yearSelect.addEventListener('change', updateSankeyChart);
        }
        if (countrySelect) {
            countrySelect.addEventListener('change', updateSankeyChart);
        }
    });

    // Export for app.js
    window.initSankeyChart = initSankeyChart;
    window.updateSankeyChart = updateSankeyChart;

})();

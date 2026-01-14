#!/usr/bin/env python3
"""
render_topic_tree.py

Read a topic-tree JSON (structure like the example) and produce an HTML file
with an interactive D3 collapsible tree. Node hover displays the topic
description and metadata.

Usage:
  python render_topic_tree.py --input topic.json --output topic_tree.html

If no input is provided, the script will try to read from stdin.
"""
import json
import argparse
import html
from pathlib import Path


HTML_TEMPLATE = r'''<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Topic Tree</title>
  <style>
    body { font-family: Arial, sans-serif; }
    .node circle { fill: #fff; stroke: steelblue; stroke-width: 2px; }
    .node text { font: 12px sans-serif; }
    .link { fill: none; stroke: #ccc; stroke-width: 2px; }
    .tooltip {
      position: absolute;
      pointer-events: none;
      background: rgba(0,0,0,0.8);
      color: #fff;
      padding: 8px;
      border-radius: 4px;
      max-width: 360px;
      font-size: 13px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      display: none;
      z-index: 1000;
    }
  </style>
</head>
<body>
  <h2>Topic Tree</h2>
  <div id="chart"></div>
  <div id="tooltip" class="tooltip"></div>

  <!-- D3 v7 -->
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
  const data = %%DATA%%;

  const tooltip = d3.select('#tooltip');

  const width = Math.max(1000, window.innerWidth - 40);
  const dx = 40; // vertical spacing between nodes
  const dy = 320; // horizontal spacing between levels
  const initialHeight = 900;
  const tree = d3.tree().nodeSize([dx, dy]);

  const root = d3.hierarchy(data, d => d.subtopics);
  root.x0 = dy / 2;
  root.y0 = 0;

  // collapse all children initially except root's immediate children
  root.children && root.children.forEach(collapse);

  const svg = d3.select('#chart').append('svg')
    .attr('width', width)
    .attr('height', initialHeight)
    .attr('viewBox', [-40, -20, width, initialHeight])
    .style('font', '14px sans-serif')
    .style('user-select', 'none');

  // Add zoomable group
  const container = svg.append('g').attr('class', 'container');
  const gLink = container.append('g').attr('fill', 'none').attr('stroke', '#555');
  const gNode = container.append('g').attr('cursor', 'pointer');

  const zoom = d3.zoom().scaleExtent([0.25, 3]).on('zoom', (event) => {
    container.attr('transform', event.transform);
  });
  svg.call(zoom);

  // compute layout once and set initial center
  tree(root);
  // center vertically on root
  const minX = d3.min(root.descendants(), d => d.x);
  const maxX = d3.max(root.descendants(), d => d.x);
  const centerY = (minX + maxX) / 2 || 0;
  // initial translate so tree is centered vertically and shifted right a bit
  const initialTransform = d3.zoomIdentity.translate(120, (initialHeight / 2) - centerY).scale(1);
  svg.call(zoom.transform, initialTransform);

  update(root);

  function update(source) {
    const duration = 250;
    const nodes = root.descendants().reverse();
    const links = root.links();

    tree(root);

    let height = Math.max(initialHeight, root.leaves().length * dx * 1.5 + 200);
    svg.transition().duration(duration).attr('height', height);

    // Links
    const link = gLink.selectAll('path').data(links, d => d.target.data.topic.name + '_' + (d.target.data.topic.metadata?.confidence_score || ''));
    link.enter().append('path')
      .attr('class', 'link')
      .attr('d', d3.linkHorizontal().x(d => d.y).y(d => d.x));
    link.exit().remove();

    // Nodes
    const node = gNode.selectAll('g.node').data(nodes, d => d.data.topic.name + '_' + (d.data.topic.metadata?.confidence_score || ''));
    const nodeEnter = node.enter().append('g')
      .attr('class', 'node')
      .attr('transform', d => `translate(${d.y},${d.x})`)
      .on('click', (event, d) => {
        // toggle children in a robust way
        if (d.children) {
          d._children = d.children;
          d.children = null;
        } else {
          d.children = d._children;
          d._children = null;
        }
        update(d);
      })
      .on('mouseover', (event, d) => showTooltip(event, d))
      .on('mousemove', (event, d) => moveTooltip(event))
      .on('mouseout', hideTooltip);

    nodeEnter.append('circle').attr('r', 10).attr('fill', d => d._children ? '#2b6cb0' : '#3182ce');
    nodeEnter.append('text')
      .attr('dy', '0.31em')
      .attr('x', d => d._children ? -16 : 16)
      .attr('text-anchor', d => d._children ? 'end' : 'start')
      .text(d => d.data.topic.name)
      .style('font-size', '15px')
      .clone(true).lower()
      .attr('stroke', 'white');

    node.exit().remove();
  }

  function collapse(d) {
    if (d.children) {
      d._children = d.children;
      d._children.forEach(collapse);
      d.children = null;
    }
  }

  function showTooltip(event, d) {
    const desc = d.data.topic.description || '';
    const conf = d.data.topic.metadata?.confidence_score;
    const source_sections = d.data.topic.metadata?.source_sections || [];
    let html = '';
    if (desc) html += `<div><strong>Description</strong><div>${escapeHtml(desc)}</div></div>`;
    if (conf !== undefined) html += `<div style="margin-top:6px"><strong>Confidence</strong>: ${conf}</div>`;
    if (source_sections && source_sections.length) html += `<div style="margin-top:6px"><strong>Sections</strong>: ${escapeHtml(source_sections.join(', '))}</div>`;
    tooltip.html(html).style('display', 'block');
    moveTooltip(event);
  }

  function moveTooltip(event) {
    const [mx, my] = d3.pointer(event);
    tooltip.style('left', (mx + 20) + 'px').style('top', (my + 20) + 'px');
  }

  function hideTooltip() { tooltip.style('display', 'none'); }

  // escape small subset of HTML
  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;');
  }
  </script>
</body>
</html>
'''


def build_html(tree_obj: dict) -> str:
    # embed JSON data directly into the template
    safe_json = json.dumps(tree_obj)
    return HTML_TEMPLATE.replace('%%DATA%%', safe_json)


def generate_topic_tree_html(topic_tree: dict, output_path: str | None = None) -> str:
  """Generate an interactive HTML representation of `topic_tree`.

  Args:
    topic_tree: A dict matching the TopicTree JSON structure.
    output_path: If provided, the HTML will also be written to this file.

  Returns:
    The generated HTML string.
  """
  html_content = build_html(topic_tree)
  if output_path:
    Path(output_path).write_text(html_content, encoding='utf-8')
  return html_content


def main():
    parser = argparse.ArgumentParser(description='Render topic JSON to interactive HTML')
    parser.add_argument('--input', '-i', help='Input JSON file (default stdin)')
    parser.add_argument('--output', '-o', help='Output HTML file', default='topic_tree.html')
    args = parser.parse_args()

    if args.input:
        p = Path(args.input)
        if not p.exists():
            raise SystemExit(f'Input file not found: {args.input}')
        tree_obj = json.loads(p.read_text(encoding='utf-8'))
    else:
        import sys
        tree_obj = json.load(sys.stdin)

    html_content = build_html(tree_obj)
    outp = Path(args.output)
    outp.write_text(html_content, encoding='utf-8')
    print(f'Wrote {outp.resolve()}')


if __name__ == '__main__':
    main()

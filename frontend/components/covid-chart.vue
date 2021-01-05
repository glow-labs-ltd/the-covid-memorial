<template>
  <svg
    id="chart"
    width="600"
    height="400"
    viewBox="0 0 600 400"
    perserveAspectRatio="xMinYMid"
  ></svg>
</template>

<script>
import * as d3 from 'd3'
export default {
  data() {
    return {}
  },
  mounted() {
    // initialize
    const chart = d3.select('#chart')
    const container = chart.node().parentNode
    this.resizeChart(chart, container)
    window.addEventListener(
      'resize',
      function () {
        this.resizeChart(chart, container)
      }.bind(this)
    )

    // generate the intial dataset
    const data = this.generateDataset(container)
    const nodes = data.map((d) => Object.create(d))
    console.log(nodes)

    // setup the collision
    const simulation = d3
      .forceSimulation(data)
      .force('charge', d3.forceManyBody())
      .force(
        'center',
        d3.forceCenter(
          container.getBoundingClientRect().width / 2,
          container.getBoundingClientRect().height / 2
        )
      )

    // create the chart
    const svg = chart
      .call(
        d3.zoom().on('zoom', function (event) {
          svg.attr('transform', event.transform)
        })
      )
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 10)
      .attr('x', (d, i) => d.x)
      .attr('y', (d, i) => d.y)
      .attr('fill', '#000000')

    // append each dot
    /*
    for (let i = 0; i < 500; i++) {
      svg
        .append('circle')
        .attr(
          'cx',
          Math.floor(Math.random() * chart.node().getBoundingClientRect().width)
        )
        .attr(
          'cy',
          Math.floor(
            Math.random() * chart.node().getBoundingClientRect().height
          )
        )
        .attr('r', 5)
        .style('fill', '#000000')
    }
    */

    simulation.on('tick', () => {
      svg.attr('cx', (d) => d.x).attr('cy', (d) => d.y)
    })
  },
  methods: {
    generateDataset(container) {
      const data = []
      for (let i = 0; i < 500; i++) {
        data[i] = {
          x: Math.floor(
            Math.random() * container.getBoundingClientRect().width
          ),
          y: Math.random() * container.getBoundingClientRect().height,
        }
      }
      return data
    },
    resizeChart(chart, container) {
      const targetWidth = container.getBoundingClientRect().width
      const targetHeight = container.getBoundingClientRect().height
      chart.attr('width', targetWidth)
      chart.attr('height', targetHeight)
    },
  },
}
</script>

<style>
#chart {
  background-color: white;
}
</style>

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
    return {
      container: null,
      currentWidth: 0,
      currentHeight: 0,
      numDots: 500,
      dotRadius: 8,
      dotColours: [
        '#73446A',
        '#F4C50F',
        '#45036E',
        '#1E447A',
        '#000000',
        '#D57004',
        '#2D5D2E',
      ],
    }
  },
  mounted() {
    // initialize the chart
    const chart = d3.select('#chart')
    this.container = chart.node().parentNode
    this.resizeChart(chart)
    window.addEventListener(
      'resize',
      function () {
        this.resizeChart(chart)
      }.bind(this)
    )

    // create the chart and append the initial dots
    const boxG = chart.append('g')
    const numBoxes = 4
    // const arr = d3.range(0, numBoxes + 1)
    const boxSize = (this.currentWidth * 4) / numBoxes
    // const boxEnter = boxG.selectAll('line').data(arr).enter()

    // generate the intial dataset
    const data = this.generateDataset(boxSize)
    const nodes = data.map((d) => Object.create(d))
    // const simulation = this.setupCollision(data)

    /*
    boxEnter
      .append('line')
      .attr('x1', function (d) {
        return d * boxSize
      })
      .attr('x2', function (d) {
        return d * boxSize
      })
      .attr('y1', -boxSize)
      .attr('y2', this.currentHeight + boxSize)
      .style('stroke', 'black')
    boxEnter
      .append('line')
      .attr('x1', -boxSize)
      .attr('x2', this.currentWidth + boxSize)
      .attr('y1', function (d) {
        return d * boxSize
      })
      .attr('y2', function (d) {
        return d * boxSize
      })
      .style('stroke', 'black')
*/

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x)
      .attr('cy', (d, i) => d.y)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x + boxSize)
      .attr('cy', (d, i) => d.y)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x + boxSize)
      .attr('cy', (d, i) => d.y + boxSize)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x)
      .attr('cy', (d, i) => d.y + boxSize)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x - boxSize)
      .attr('cy', (d, i) => d.y)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x - boxSize)
      .attr('cy', (d, i) => d.y - boxSize)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x)
      .attr('cy', (d, i) => d.y - boxSize)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x + boxSize)
      .attr('cy', (d, i) => d.y - boxSize)
      .attr('fill', (d, i) => d.colour)

    boxG
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', this.dotRadius)
      .attr('cx', (d, i) => d.x - boxSize)
      .attr('cy', (d, i) => d.y + boxSize)
      .attr('fill', (d, i) => d.colour)

    const zoom = d3
      .zoom()
      .scaleExtent([0.1, 2])
      .on('zoom', function (event) {
        const transform = event.transform
        const scale = transform.k
        const dx = transform.x % (boxSize * scale)
        const dy = transform.y % (boxSize * scale)
        // svg.attr(
        //  'transform',
        //  'translate(' + dx + ',' + dy + ')scale(' + scale + ')'
        // )
        boxG.attr(
          'transform',
          'translate(' + dx + ',' + dy + ')scale(' + scale + ')'
        )
      })

    chart.call(zoom)

    // update the x and y deltas each tick (for collisions)
    // simulation.on('tick', () => {
    //   svg.attr('cx', (d) => d.x).attr('cy', (d) => d.y)
    // })
  },
  methods: {
    generateDataset(boxSize) {
      const data = []
      for (let i = 0; i < this.numDots; i++) {
        data[i] = {
          x: Math.floor(Math.random() * boxSize),
          y: Math.floor(Math.random() * boxSize),
          colour: this.dotColours[
            Math.floor(Math.random() * this.dotColours.length)
          ],
        }
      }
      return data
    },
    setupCollision(data) {
      return d3.forceSimulation(data).force('charge', d3.forceManyBody())
      // .force(
      //   'center',
      //   d3.forceCenter(this.currentWidth / 2, this.currentHeight / 2)
      // )
    },
    resizeChart(chart) {
      this.currentWidth = this.container.getBoundingClientRect().width
      this.currentHeight = this.container.getBoundingClientRect().height
      chart.attr('width', this.currentWidth)
      chart.attr('height', this.currentHeight)
    },
  },
}
</script>

<style>
#chart {
  background-color: #f5f6f5;
}
</style>

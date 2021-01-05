<template>
  <div class="container">
    <!--
    <div>
      <Logo />
      <h1 class="title">the-covid-memorial</h1>
      <div class="links">
        <a
          href="https://nuxtjs.org/"
          target="_blank"
          rel="noopener noreferrer"
          class="button--green"
        >
          Documentation
        </a>
        <a
          href="https://github.com/nuxt/nuxt.js"
          target="_blank"
          rel="noopener noreferrer"
          class="button--grey"
        >
          GitHub
        </a>
      </div>
    </div>
    -->
    <svg
      id="chart"
      width="600"
      height="400"
      viewBox="0 0 600 400"
      perserveAspectRatio="xMinYMid"
    ></svg>
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  data() {
    return {
      nodes: [],
    }
  },
  mounted() {
    const chart = d3.select('#chart')
    // const aspect =
    //  chart.node().getBoundingClientRect().width /
    //  chart.node().getBoundingClientRect().height
    const container = d3.select('.container')
    this.resizeChart(chart, container)
    window.addEventListener(
      'resize',
      function () {
        this.resizeChart(chart, container)
      }.bind(this)
    )

    const svg = chart
      .call(
        d3.zoom().on('zoom', function (event) {
          svg.attr('transform', event.transform)
        })
      )
      .append('g')

    for (let i = 0; i < 2000; i++) {
      this.nodes.push(
        svg
          .append('circle')
          .attr(
            'cx',
            Math.floor(
              Math.random() * chart.node().getBoundingClientRect().width
            )
          )
          .attr(
            'cy',
            Math.floor(
              Math.random() * chart.node().getBoundingClientRect().height
            )
          )
          .attr('r', 5)
          .style('fill', '#000000')
      )
    }
  },
  methods: {
    resizeChart(chart, container) {
      const targetWidth = container.node().getBoundingClientRect().width
      const targetHeight = container.node().getBoundingClientRect().height
      chart.attr('width', targetWidth)
      chart.attr('height', targetHeight) // Math.round(targetWidth / aspect))
    },
  },
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 400;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

#chart {
  background-color: white;
}
</style>

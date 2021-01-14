<template>
  <canvas></canvas>
</template>

<script>
import * as d3 from 'd3'
import { mapState } from 'vuex'

export default {
  data() {
    return {
      width: null,
      height: null,
      transform: null,
      opacityScale: null,
      canvas: null,
      zoom: null,
      minZoom: 1,
      maxZoom: 2,
      maxDots: 2000,
      radius: d3.randomInt(4, 16),
      transitionTime: 3000,
    }
  },
  computed: mapState(['overviewTransition']),
  watch: {
    overviewTransition() {
      this.canvas
        .transition()
        .duration(this.transitionTime)
        .call(this.zoom.transform, d3.zoomIdentity.scale(this.maxZoom - 0.01))
        .on(
          'end',
          function () {
            this.$store.commit('setOverview', false)
          }.bind(this)
        )
    },
  },
  mounted() {
    this.width = window.innerWidth
    this.height = window.innerHeight - 80
    this.canvas = d3
      .select('canvas')
      .attr('width', this.width)
      .attr('height', this.height)
      .attr('initial-scale', this.maxZoom)
    const context = this.canvas.node().getContext('2d')
    this.calculateZoomLevels()

    const radii = Array.from({ length: 800 }, this.radius)
    const nodes = radii.map((r) => ({ r }))
    this.transform = d3.zoomIdentity
    this.opacityScale = d3
      .scaleLinear()
      .domain([this.minZoom, this.maxZoom])
      .range([1, 0])

    const simulation = d3
      .forceSimulation(nodes)
      .alphaTarget(0.2)
      .velocityDecay(0.5)
      .force('x', d3.forceX().strength(0.001))
      .force('y', d3.forceY().strength(0.001))
      .force(
        'collide',
        d3.forceCollide().radius((d) => d.r + 1)
      )
      .on(
        'tick',
        function () {
          this.ticked(context, nodes)
        }.bind(this)
      )

    this.zoom = d3
      .zoom()
      .scaleExtent([this.minZoom, this.maxZoom])
      .on(
        'zoom',
        function (event) {
          this.transform = event.transform
          if (this.transform.k >= this.maxZoom) {
            this.$store.commit('setOverview', false)
          }
          this.ticked(context, nodes)
        }.bind(this)
      )
    d3.select(this.canvas.node()).call(this.zoom)

    window.addEventListener(
      'resize',
      function () {
        this.resizeCanvas(this.canvas)
      }.bind(this)
    )

    this.canvas
      .call(this.zoom.transform, d3.zoomIdentity.scale(this.maxZoom - 0.01))
      .transition()
      .delay(1500)
      .duration(this.transitionTime)
      .call(this.zoom.transform, d3.zoomIdentity.scale(this.minZoom))

    setTimeout(
      function () {
        this.spawnMoreDots(100, nodes, simulation)
      }.bind(this),
      3000
    )
  },
  methods: {
    calculateZoomLevels() {
      const shortestEdge = Math.min(this.width, this.height)
      this.minZoom = shortestEdge / 800
    },
    spawnMoreDots(interval, nodes, simulation) {
      setInterval(
        function () {
          this.addNode(nodes, simulation)
        }.bind(this),
        interval
      )
    },
    addNode(nodes, sim) {
      if (nodes.length < this.maxDots) {
        nodes.push({ r: this.radius() })
        sim.nodes(nodes)
      }
    },
    ticked(context, nodes) {
      context.clearRect(0, 0, this.width, this.height)
      context.save()

      context.globalAlpha = this.opacityScale(this.transform.k)
      context.translate(this.width / 2, this.height / 2)
      context.scale(this.transform.k, this.transform.k)
      context.beginPath()
      for (const d of nodes) {
        context.moveTo(d.x + d.r, d.y)
        context.arc(d.x, d.y, d.r, 0, 2 * Math.PI)
      }
      context.fillStyle = '#333333'
      context.fill()
      context.restore()
    },
    resizeCanvas(canvas) {
      this.width = window.innerWidth
      this.height = window.innerHeight
      canvas.attr('width', this.width).attr('height', this.height)
    },
  },
}
</script>

<style lang="scss" scoped></style>

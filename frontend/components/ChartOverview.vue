<template>
  <canvas></canvas>
</template>

<script>
import * as d3 from 'd3'

export default {
  data() {
    return {
      width: null,
      height: null,
      transform: null,
      minZoom: 1,
      maxZoom: 2,
      maxDots: 2000,
      radius: d3.randomInt(4, 16),
    }
  },
  mounted() {
    this.width = window.innerWidth
    this.height = window.innerHeight - 80
    const canvas = d3
      .select('canvas')
      .attr('width', this.width)
      .attr('height', this.height)
      .attr('initial-scale', this.maxZoom)
    const context = canvas.node().getContext('2d')

    const radii = Array.from({ length: 800 }, this.radius)
    const nodes = radii.map((r) => ({ r }))
    this.transform = d3.zoomIdentity

    const simulation = d3
      .forceSimulation(nodes)
      .alphaTarget(0.1)
      .velocityDecay(0.3)
      .force('x', d3.forceX().strength(0.002))
      .force('y', d3.forceY().strength(0.002))
      .force(
        'collide',
        d3.forceCollide().radius((d) => d.r + 0.5)
      )
      .on(
        'tick',
        function () {
          this.ticked(context, nodes)
        }.bind(this)
      )

    const zoom = d3
      .zoom()
      .scaleExtent([this.minZoom, this.maxZoom])
      .on(
        'zoom',
        function (event) {
          this.transform = event.transform
          if (this.transform.k > this.maxZoom - 0.1) {
            this.$emit('zoomIn')
          }
          this.ticked(context, nodes)
        }.bind(this)
      )

    d3.select(canvas.node()).call(zoom)
    this.transform.k = this.maxZoom - 0.11
    this.ticked(context, nodes)

    setInterval(
      function () {
        this.addNode(nodes, simulation)
      }.bind(this),
      2000
    )

    window.addEventListener(
      'resize',
      function () {
        this.resizeCanvas(canvas)
      }.bind(this)
    )
  },
  methods: {
    addNode(nodes, sim) {
      if (nodes.length < this.maxDots) {
        nodes.push({ r: this.radius() })
        sim.nodes(nodes)
      }
    },
    ticked(context, nodes) {
      context.clearRect(0, 0, this.width, this.height)
      context.save()
      context.globalAlpha = this.maxZoom - this.transform.k
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

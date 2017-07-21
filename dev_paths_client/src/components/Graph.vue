<template>
  <div id="network-graph"></div>
</template>

<script>
  import * as $ from 'jquery';
  import * as Sigma from 'sigma';

  export default {
    name: 'network-graph',
    data() {
      return {
        sigmaInstance: null,
        graphData: null,
      };
    },
    mounted() {
      let sigma;
      let graphData;

      // eslint-disable-next-line new-cap
      $.get('http://localhost:8003/graph', (graph) => {
        graphData = graph;

        sigma = new Sigma({
          graph: graphData,
          container: 'network-graph',
          settings: {
            defaultNodeColor: '#ec5148',
          },
        });

        sigma.bind('clickNode', (evt) => {
          const lang = evt.data.node.id;

          $.get(`http://localhost:8003/path/${encodeURIComponent(lang)}`, (data) => {
            graphData.edges = data;
            sigma.graph.clear();
            sigma.graph.read(graphData);
            sigma.refresh();
          });
        });
        sigma.refresh();

        this.sigmaInstance = sigma;
        this.graphData = graphData;
      });
    },
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #network-graph {
    width: 400px;
    height: 400px;
  }
</style>

<template>
  <div id="div">
    <canvas id="myfirstchart"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js";
export default {
  data: function() {
    return {
      myData: {
        labels: ["及时性", "充分性", "真实性", "相关性", "其他"],
        datasets: [
          {
            label: "该公司评分",
            data: [],
            backgroundColor: ["rgba(94,195,235,0.5)"],
            borderColor: ["rgba(31, 129, 168,0.9)"],
            pointBackgroundColor: [
              "rgba(31, 129, 168,1)",
              "rgba(31, 129, 168,1)",
              "rgba(31, 129, 168,1)",
              "rgba(31, 129, 168,1)",
              "rgba(31, 129, 168,1)"
            ],
            pointRadius: ["4", "4", "4", "4", "4"],
            pointHoverRadius: ["6", "6", "6", "6", "6"]
          },
          {
            label: "行业平均评分",
            data: [],
            backgroundColor: ["rgba(241,123,196,0.5)"],
            borderColor: ["rgba(238, 24, 156,0.9)"],
            pointBackgroundColor: [
              "rgba(238, 24, 156,0.5)",
              "rgba(238, 24, 156,0.5)",
              "rgba(238, 24, 156,0.5)",
              "rgba(238, 24, 156,0.5)",
              "rgba(238, 24, 156,0.5)"
            ],
            pointRadius: ["4", "4", "4", "4", "4"],
            pointHoverRadius: ["6", "6", "6", "6", "6"]
          }
        ]
      }
    };
  },
  mounted: function() {
    var ctx = document.getElementById("myfirstchart").getContext("2d");
    this.myData.datasets[0].data = this.companyScoreData;
    this.myData.datasets[1].data = this.averScoreData;
    var myRadar = new Chart(ctx, {
      type: "radar",
      data: this.myData,
      options: {
        //刻度轴相关配置
        scale: {
          ticks: {
            suggestedMin: 60,
            suggestedMax: 100
          },
          pointLabels: {
            //外边一圈字体的颜色
            fontSize: 18
          },
          display: true
        },
        //图例配置
        legend: {
          labels: {
            fontSize: 18
          }
        },
        tootips:{
          mode:'dataset'
        }
      }
    });
  },
  props: {
    companyScoreData: {
      type: Array,
      default: () => {
        return [65, 75, 85, 69, 86];
      }
    },
    averScoreData: {
      type: Array,
      default: () => {
        return [60, 68, 85, 86, 67];
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#div {
  width: 100%;
  height: 100%;
  text-align: center;
}
</style>

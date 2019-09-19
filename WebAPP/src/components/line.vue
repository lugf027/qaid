<template>
  <div id='chart-box'>
    <canvas ref="myChart"></canvas>
    <br />
  </div>
</template>

<script>
import "chart.js";
export default {
  name: "tChart",
  data: function() {
    return {
      mData: {
        labels: [],
        datasets: [
          {
            label: "公司评分",
            fill: false,
            backgroundColor: "#3399ff",
            borderColor: "#3399ff",
            lineTension: 0.3,
            yAxisID: "mark",
            data: []
          },
          {
            label: "行业平均水平",
            fill: false,
            backgroundColor: "#FF69B4",
            borderColor: "#FF69B4",
            yAxisID: "mark",
            data: []
          },
          {
            label: "股价",
            fill: true,
            backgroundColor: "rgba(255,0,0,0.2)",
            borderColor: "rgba(255,0,0,0.5)",
            yAxisID: "price",
            data: []
          }
        ]
      },
      mOption: {
        responsive: true,
				title: {
					display: false,
					text: ' '
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
        scales: {
          yAxes: [
            {
              type: "linear",
              display: true,
              position: "left",
              id: "mark",
              axisLabel:{
                interval:0
              },
              scaleLabel: {
							  display: true,
                labelString: '得分/%',
                fontSize:16
						  },
              ticks:{
                max: 100,
                min: 0,
              }
              
              // gridLines: {
              //   show: false
              // }
            },
            {
              type: "linear",
              display: true,
              position: "right",
              suggestedMin: 0,
              id: "price",
              ticks:{
                min: 0,
                suggestedMax:30,
                callback: function(value, index, values) {
                  return '￥' + value+'.00';
                }
              },
              scaleLabel: {
							  display: true,
                labelString: '股票价格/￥',
                fontSize:16
              },
              gridLines: {
                display: false
              }
            }
          ]
        }
      }
    };
  },
  props: {

    //年份；x轴标签
    years: {
      type: Array,
      default: () => {
        return ["2016", "2017","2018", "2019"];
      }
    },
    //公司得分数据
    companyData: {
      type: Array,
      default: () => {
        return [60, 48, 90, 55];
      }
    },
    //行业平均分数据
    industryData: {
      type: Array,
      default: () => {
        return [65, 54, 86, 60];
      }
    },
    //公司股票价格数据
    stockData: {
      type: Array,
      default: () => {
        return [18.5, 13.9, 19.8, 25.6];
      }
    }
  },
  mounted: function() {
    var ctx = this.$refs.myChart.getContext("2d");
    // console.log(this.companyData)
    console.log(this.mOption);
    this.mData.labels = this.years;
    this.mData.datasets[0].data = this.companyData;
    this.mData.datasets[1].data = this.industryData;
    this.mData.datasets[2].data = this.stockData;

    var mChart = new Chart(ctx, {
      type: "line",
      data: this.mData,
      options: this.mOption
    });
  },
  methods: {
    search: function() {
      console.log(this.$refs["myChart"]);
    }
  }
};
</script>



<style lang="" scoped>
  #chart-box{
    margin-left: 5%;
    text-align: center;
    width: 90%
  }
  canvas{
    display: inline;
    position: relative;
  }
</style>
<template>
    <div>
        <canvas ref="myChart"></canvas>
    </div>
</template>

<script>
import "chart.js"

export default {
    name: 'tChart',
    data:function(){
        return{
            mData:{
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [
            {
            label: "My First dataset",
            // fillColor: "rgba(255,255,255,0.2)",
            // strokeColor: "rgba(20,20,25,1)",
            // pointColor: "rgba(220,220,220,1)",
            // pointStrokeColor: "#fff",
            // pointHighlightFill: "#fff",
            // pointHighlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
            label: "My Second dataset",
            // strokeColor: "rgba(151,187,205,1)",
            // pointColor: "rgba(151,187,205,1)",
            // pointStrokeColor: "#fff",
            // pointHighlightFill: "#fff",
            // pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 100]
            }
            ]
            }
        }
    },
    mounted:function(){
        var ctx=this.$refs.myChart.getContext("2d")
        var mChart=new Chart(ctx,{
            type:"line",
            data:this.mData
        })
    },
    methods:{
        search:function(){
             console.log(this.$refs['myChart'])
        }
    }
}
</script>



<style lang="" scoped>
</style>

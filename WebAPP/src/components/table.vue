<template>
    <div id='table-box'>
        <Table stripe border :columns="columns" :data="datas" class="table-display"></Table> 
    </div>
</template>

<script>
export default {
    data:function(){
        return{
            columns:[
                {
                    title:'指标',
                    key:'title'
                }
            ]
        }
    },
    props:{
        years:{
            type:Array,
            default:()=>{
                return[
                    2016,2017,2018
                ]
            }
        },
        datas: {
            type: Array,
            default: () => {
                return [
                    {
                        title:'指标1',
                        value:[1,0,1],
                    },
                    {
                        title:'指标2',
                        value:[1,0,1],
                    },
                    {
                        title:'指标3',
                        value:[1,0,1],
                    },
                    {
                        title:'指标4',
                        value:[1,0,1],
                    },
                    {
                        title:'指标5',
                        value:[1,0,1],
                    },
                ];
            }
    },
    },
    mounted:function(){
        for(index in this.datas){
            for(year in this.years){
                if(this.datas[index].value[year]==0){
                    this.datas[index][this.years[year]]='否'
                }else{
                    this.datas[index][this.years[year]]='是'
                }
            }
        }
        var index
        for (index in this.years){
            var year="'"+this.years[index]+"'"
            console.log(year)
            this.columns.push({
                title:String(this.years[index]),
                key:String(this.years[index]),
            })
        }
    }

}
</script>


<style scoped>
#table-box{

}
 .table-display{
     /* display: inline; */
 }
</style>
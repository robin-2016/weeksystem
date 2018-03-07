$(function () {
    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();
    //2.初始化Button的点击事件
    // var oButtonInit = new ButtonInit();
    // oButtonInit.Init();
    //按钮插入操作
    var oBtn_insert = document.getElementById('insButton');
    oBtn_insert.onclick = ROWINS;
    //删除按钮操作
    var oBtn_add = document.getElementById('btn_delete');
    oBtn_add.onclick = ROWDEL;
});
var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_departments').bootstrapTable({
            url: '/data/lastzhoubao',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParamsType:"undefined",
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 18,                       //每页的记录行数（*）
            // pageList: [20, 40, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 823,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                field: 'project',
                title: '所属项目',
                editable:{
                    type:'select',
                    // sourceCache:true,
                    // async:false,
                    source: function () {
                        var result = [];
                         $.ajax({
                            url:'/groups',
                            type:'GET',
                            async:false,
                            // dataType:'JSON',
                            data:{},
                            success:function (data) {
                                $.each(data,function (key,value) {
                                    result.push({value:parseInt(key),text:value});
                                });
                            }
                        });
                         return result;
                    },
                    validate: function (v) {
                        if (!v) return '项目不能为空';
                    }
                }
            }, {
                field: 'worktime',
                title: '当日工作量',
                editable:{
                    type:'text',
                    title:'当日工作量',
                    validate: function (v) {
                        var re = /^[1-9]$|^1[0-9]$|^2[0-4]$|^[0-9]\.\d$|^1[0-9]\.\d$|^2[0-3]\.\d$/g;
                        var result = re.test(v);
                        if (!result) return '工作量超出1-24范围';
                    }
                }
            }, {
                field: 'completed',
                title: '周完成情况',
                editable:{
                    type:'text',
                    title:'周完成情况',
                    validate: function (v) {
                        var re = /^100$|^\d$|^[1-9]\d$/g;
                        if ( !re.test(v)) return '周完成情况超出0-100范围';
                    }
                }
            }, {
                field: 'something',
                title: '工作内容',
                width: "50%",
                editable:{
                    type:'text',
                    title:'工作内容',
                    mode:'inline',
                    width: "100%",
                    validate: function (v) {
                        if (!v) return '工作内容不能为空';
                    }
                }
            },{
                field: 'week',
                title: '时间记录',
                editable:{
                    type:'select',
                    source:[
                        {value:0,text:'星期一'},
                        {value:1,text:'星期二'},
                        {value:2,text:'星期三'},
                        {value:3,text:'星期四'},
                        {value:4,text:'星期五'},
                        {value:5,text:'星期六'},
                        {value:6,text:'星期日'}
                    ],
                    validate: function (v) {
                        if (!v) return '星期不能为空';
                    }
                }
            }],
            onEditableSave: function (field,row,oldValue,$el) {
                // console.log(row)
                $.ajax({
                    type:"POST",
                    url:"/post",
                    data:row,
                    dataType:"JSON",
                    success:function (data,status) {
                        if (status == "success") {
                            console.log("提交成功！");
                        }
                    },
                    error:function () {
                        console.log("编辑失败！")
                    },
                    complete:function () {
                        // $('#tb_departments').bootstrapTable('refresh');
                    }
                });
            }
        });
    };
    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            // limit: params.limit,   //页面大小
            pageNumber: params.pageNumber  //页码
            // departmentname: $("#txt_search_departmentname").val(),
            // statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
    // $("#tb_departments").on('save.newuser',function () {
    //     var that =this;
    //     setTimeout(function () {
    //         $(that).closest('tr').next().find('#tb_departments').editable('show');
    //     },200);
    // });
};
// var ButtonInit = function () {
//     var oInit = new Object();
//     var postdata = {};
//     oInit.Init = function () {
//         //初始化页面上面的按钮事件
//     };
//     return oInit;
// };
var ROWDEL = function () {
    var ids = $.map($("#tb_departments").bootstrapTable('getSelections'),function (row) {
        return row.id;
    });
        if (ids.length <= 0){
        alert("请选择一行删除！");
        return;
    }
    var idsstr = ids.toString();
    $(function () {
        var msg = "确定要删除？";
        if (confirm(msg) == true){
            $.ajax({
                url:'/del/newdata',
                type:'POST',
                data:{'id':idsstr},
                dataType:'JSON'
                })
                .done(function () {
                    $("#tb_departments").bootstrapTable('remove',{
                            field:'id',
                            values:ids
                            });
                    $('#tb_departments').bootstrapTable('refresh');
                })
                .fail(function () {
                    $("#tb_departments").bootstrapTable('remove',{
                            field:'id',
                            values:ids
                            });
                    $('#tb_departments').bootstrapTable('refresh');
                });
        }
    });
};
var ROWINS = function () {
    // $(".form").submit()
    //表单验证
    var yz1 = false;
    var yz2 = false;
    var yz3 = false;
    var something = $("#something");
    var worktime = $("#worktime");
    var  completed = $("#completed");
    if (something.val() ==null || something.val() ==""){
        something.next().remove();
        something.parent().addClass("has-error");
        something.parent().append("<p class=\"help-block\">工作内容不能为空！</p>");
    }
    else if (something.val().length > 400){
        something.next().remove();
        something.parent().addClass("has-error");
        something.parent().append("<p class=\"help-block\">工作内容数据过长！</p>");
    }
    else {
        something.parent().removeClass("has-error");
        something.next().remove();
        yz1 = true;
    }
    var worktiemre = /^[1-9]$|^1[0-9]$|^2[0-4]$|^[0-9]\.\d$|^1[0-9]\.\d$|^2[0-3]\.\d$/g;
    if (!worktiemre.test(worktime.val())){
        worktime.next().remove();
        worktime.parent().addClass("has-error");
        worktime.parent().append("<p class=\"help-block\">工作量不能为空或超出1-24范围！</p>");
    }
    else {
        worktime.parent().removeClass("has-error");
        worktime.next().remove();
        yz2 = true;
    }
    var completedre = /^100$|^\d$|^[1-9]\d$/g;
    if (!completedre.test(completed.val())) {
        completed.next().remove();
        completed.parent().addClass("has-error");
        completed.parent().append("<p class=\"help-block\">周完成情况不能为空或超出0-100范围！</p>");
    }
    else {
        completed.parent().removeClass("has-error");
        completed.next().remove();
        yz3 = true;
    }
    if (yz1 ==false || yz2 == false || yz3 == false){
        return false;
    }
    var data = $(".form").serialize();
    $.ajax({
        type:"POST",
        url:"/insert/lastpost",
        data: data,
        success : function () {
            // console.log("提交成功！");
            $("#myModal").modal('hide');
            $('#tb_departments').bootstrapTable('refresh');
            // $("#myModal").removeData("bs.modal");
            $("#myModal").on("hidden.bs.modal",function () {
                //使用js赋值
                // document.getElementById('worktime').value='';
                // document.getElementById('something').value='';
                //使用jQuery赋值
                $("#worktime").val("");
                $("#something").val("");
            });
        },
        error:function () {
            console.log("提交失败！");
            // return true;
        },
        complete:function () {
            // return true;
        }
    });
};
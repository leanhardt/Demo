$(function () {
    $("#submit").click(function (event) {
        //evemt.prevemtDefault
        //是阻止按钮默认的提交表单的事件
        event.preventDefault();
        // 获取标签
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwdE2 = $("input[name=newpwd2]");
        //获取值
        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwdE2.val();

        Flask_Demo.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                if(data['code'] == 200){
                    fdalert.alertSuccessToast("修改成功！");
                    //修改成功后清空输入框
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwdE2.val("");
                }else{
                    var message = data['message'];
                    fdalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                fdalert.alertNetworkError();
            }
        })
    })
})
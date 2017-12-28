$(function () {
    $("#submit").onclick = function () {
        var username = $("#username").val();
        // var passwd = $("#passwd").val();
        var usernamere = /^[\u4E00-\u9FA5].*$|^[\u4E00-\u9FA5].*\d$/g;
        console.log(username)
        if (!usernamere.test(username)) {
            console.log("用户名为汉字或者汉字加一位数字！")
            alert("用户名为汉字或者汉字加一位数字！");
            return false;
        }
    };
});
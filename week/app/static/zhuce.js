$(function () {
    var yz1=false;
    var yz2=false;
    var usernameinput = $("#username");
    usernameinput.blur(function () {
        var username = usernameinput.val();
        var usernamere = /^[\u4E00-\u9FA5]+$|^[\u4E00-\u9FA5]+\d\d$/g;
        // console.log(username)
        if (!usernamere.test(username)) {
            usernameinput.next().remove();
            usernameinput.parent().addClass("has-error");
            // <p class="help-block">两次密码不相同！</p>
            usernameinput.parent().append("<p class=\"help-block\">用户名为汉字或者汉字加两位数字！</p>");
        }
        else {
            usernameinput.parent().removeClass("has-error");
            usernameinput.next().remove();
           yz1 = true;
        }
    });
    var passwdinput = $("#passwd");
    var passwd2input = $("#passwd2");
    passwd2input.blur(function () {
        if (passwdinput.val() != passwd2input.val()){
            passwdinput.next().remove();
            passwdinput.parent().addClass("has-error");
            passwd2input.parent().addClass("has-error");
            passwdinput.parent().append("<p class=\"help-block\">两次密码不相同！</p>");
        }
        else {
            passwdinput.parent().removeClass("has-error");
            passwd2input.parent().removeClass("has-error");
            passwdinput.next().remove();
            yz2 = true;
        }
    });
    if (yz1 ==false || yz2 == false){
        return false;
    }
});
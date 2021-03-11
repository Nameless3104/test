<%@ page import="day04.service.UserService" %>
<%@ page import="day04.service.UserServiceImpl" %>
<%@ page import="java.util.List" %>
<%@ page import="day04.po.User" %><%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/5
  Time: 20:50
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<%--    一般不会这么写，只是一个思路--%>
<%
    UserService userService = new UserServiceImpl();
    List<User> list = userService.queryAll(null);
%>
<form>
    <table width="80%" cellpadding="0" cellspacing="0" border="1">
        <tr>
            <td>id</td>
            <td>用户名</td>
            <td>密码</td>
            <td>操作</td>
        </tr>
        <%
            for(User u:list){
        %>

        <tr>
            <td><%=u.getaId()%></td>
            <td><%=u.getaName()%></td>
            <td><%=u.getaPassword()%></td>
            <td>操作</td>
        </tr>
        <%
            }
        %>
    </table>
</form>
</body>
</html>

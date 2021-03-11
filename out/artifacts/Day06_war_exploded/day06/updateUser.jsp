<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/7
  Time: 20:15
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>

<body>
<h1>用户修改</h1>
<form action="${pageContext.request.contextPath}/modifyUser.do">
    <input type="hidden" name="id" value="${user.aId}">
    用户名: <input type="text" name="username" value="${user.aName}"/><br>
    密码: <input type="text" name="pwd" value="${user.aPassword}"/><br>
    <input type="submit" value="提交">
</form>
</body>
</html>

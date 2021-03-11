<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/5
  Time: 20:54
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <meta charset="utf-8">
    <title>用户登录</title>
</head>

<script>
    function checkAll(){
        return true;
    }
</script>

<body>
<h1>用户登录</h1>

<%--    <a href="/Day04_war_exploded/login.do">跳转</a>--%>

<%--    ${pageContext.request.contextPath}--%>


<%--${aUser} <br>--%>

<c:if test="${not empty aUser}">
    <%
        request.getRequestDispatcher("/query06.do").forward(request, response);
    %>
</c:if>

<form action="${pageContext.request.contextPath}/login06.do" method="post" onsubmit="return checkAll();">
<%--    ID: <input type="text" name="id"/> <br>--%>
    用户名: <input type="text" name="username" /><br>
    密码: <input type="password" name="pwd" /><br>
    兴趣爱好: <input type="checkbox" value="1" name="likes" /> 钓鱼
    <input type="checkbox" value="2" name="likes" /> 煮鱼
    <input type="checkbox" value="3" name="likes" /> 吃鱼
    <br>
    <input type="submit" value="提交" />
</form>
</body>
</html>

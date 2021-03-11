<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/6
  Time: 19:16
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
    <title>Title</title>
</head>
<body>

需求：传过来1和2， 1代表男，2代表女 <br>
<c:set var="sex" value="2"></c:set>
输出值为：${sex} <br>

<%--<c:if test="${sex == 1}">男</c:if>--%>
<%--<c:if test="${sex == 2}">女</c:if>--%>
<br>

<%--<c:if test="${sex == 1}">checked</c:if>--%>
<%--<c:if test="${sex == 2}">checked</c:if>--%>

性别：<input type="radio" name="sex" value="1" <c:if test="${sex == 1}">checked</c:if>
>男
<input type="radio" name="sex" value="2" <c:if test="${sex == 2}">checked</c:if>
>女

</body>
</html>

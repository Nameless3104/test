<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/6
  Time: 16:32
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
    <title>Title</title>
</head>
<body>

<c:set var="age" value="38"></c:set>

年龄为：${age} <br>
<c:choose>
    <c:when test="${0 <= age && age < 20}">年龄在10~20之间</c:when>
    <c:when test="${20 <= age && age < 40}">年龄在20~40之间</c:when>
    <c:when test="${40 <= age && age < 60}">年龄在40~60之间</c:when>
    <c:when test="${60 <= age && age < 80}">年龄在60~80之间</c:when>
</c:choose>

</body>
</html>

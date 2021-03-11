<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/5
  Time: 21:27
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<html>
<head>
    <title>Title</title>
</head>
<body>
<form>

    <table width="80%" border="1" cellpadding="0" cellspacing="0">
        <tr>
            <td>id</td>
            <td>用户名</td>
            <td>密码</td>
            <td>操作</td>
        </tr>

        <c:forEach var="li" items="${userList}">
            <tr>
                <td>${li.aName}</td>
                <td>${li.aPassword}</td>
                <td>${li.aId}</td>
                <td>操作</td>
            </tr>
        </c:forEach>

    </table>
</form>
</body>
</html>

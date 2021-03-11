<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/6
  Time: 16:27
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%--听说不加这个isELIgnored会有问题，但是其实没加也没问题--%>
<%--<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>--%>
<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<html>
<head>
    <title>Title</title>
</head>
<body>

<c:set var="theVar" value="theValue"></c:set>
通过el表达式获取值: ${theVar} <br>

<c:set var="age" value="18"></c:set>


<c:if test="${age>18}">年龄大于18岁</c:if>
<c:if test="${age<=18}">年龄小于等于18岁</c:if>

</body>
</html>

<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/6
  Time: 16:23
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>

<%
    request.setAttribute("aKey", "theValue");
%>

<%=request.getAttribute("aKey")%> 这个不要 <br>

<%--这个是el表达式--%>
${aKey}

</body>
</html>

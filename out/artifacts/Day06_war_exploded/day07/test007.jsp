<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/6
  Time: 19:17
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>

获取page的值 <%=pageContext.getAttribute("pageKey")%> <br>
获取request的值 <%=request.getAttribute("requestKey")%> <br>
获取session的值 <%=session.getAttribute("sessionKey")%> <br>
获取application的值 <%=application.getAttribute("applicationKey")%> <br>

获取form表单<%=request.getParameter("cccc")%>

</body>
</html>

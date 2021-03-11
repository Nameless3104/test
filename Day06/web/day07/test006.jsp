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

<%
    //这些没有new对象就可以使用的，称之为jsp内置对象  9大内置对象
//    out           输出
//    request       请求对象
//    response      响应对象
//    application   全局servlet上下文对象
//    page          代表当前jsp，即this
//    pageContext   jsp上下文
//    session       代表一次会话
//    config        Servlet配置对象
//    exception     所捕获的页面对象
%>

通过page存值 <%pageContext.setAttribute("pageKey", "pageValue");%> <br>
通过request存值 <%request.setAttribute("requestKey", "requestValue");%> <br>
通过session存值 <%session.setAttribute("sessionKey", "sessionValue");%> <br>
通过application存值 <%application.setAttribute("applicationKey", "applicationValue");%> <br>

获取page的值 <%=pageContext.getAttribute("pageKey")%> <br>
获取request的值 <%=request.getAttribute("requestKey")%> <br>
获取session的值 <%=session.getAttribute("sessionKey")%> <br>
获取application的值 <%=application.getAttribute("applicationKey")%> <br>

<form action="test007.jsp" method="post">

    <input type="text" name="cccc" value="dddd">
    <input type="submit" value="提交">

</form>


</body>
</html>

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

<%--session失效时间 默认30分钟
    第一种修改失效时间：在tomcat的config中的web.xml，修改下面的
    这个的单位是分钟，即默认为30分钟
        <session-config>
            <session-timeout>30</session-timeout>
        </session-config>
    第二种修改失效时间，在web.xml中修改，只对当前工程有效

    第三种在servlet文件中修改
--%>
这是test008
<%
    HttpSession session1 = request.getSession(true);
    session1.setMaxInactiveInterval(10); // 这个的单位是秒
    session1.setAttribute("cccc", "10秒结束");
%>


</body>
</html>

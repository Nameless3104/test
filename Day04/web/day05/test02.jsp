<%--
  Created by IntelliJ IDEA.
  User: MI
  Date: 2021/3/5
  Time: 20:30
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>

<%--<%
    int[] num = {1, 2, 3, 4};
%>

<%
    for (int i = 0; i < num.length; i++) {
%>

    <%=num[i]%><br>

<%}%>--%>


<%
    int[] nums = {2, 2, 3, 4};
    for (int num : nums) {
%>

<%=num%><br>

<%}%>
</body>
</html>

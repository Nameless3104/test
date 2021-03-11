package day06.action.day10;

import day06.po.User;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

@WebServlet("/userToJson.do")
public class UserToJSONAction extends HttpServlet {
    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String encoding = this.getServletContext().getInitParameter("encoding");
        req.setCharacterEncoding(encoding);
        resp.setContentType("text/html;charset=" + encoding);

        PrintWriter out = resp.getWriter();
        User user = new User();

        JSONObject json = JSONObject.fromObject(user);
        out.println(json);
        out.println("<br>");

        User user2 = new User("张三", "123");
        User user3 = new User("李四", "456");
        List<User> list = new ArrayList<User>();
        list.add(user2);
        list.add(user3);

        JSONArray jsonArray = JSONArray.fromObject(list);
        out.println(jsonArray);
    }
}

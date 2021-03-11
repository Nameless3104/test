package day04.action;

import day04.po.User;
import day04.service.UserService;
import day04.service.UserServiceImpl;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.List;

public class UserQueryAction extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String encoding = this.getServletContext().getInitParameter("encoding");
        resp.setContentType("text/html;charset=" + encoding);
        req.setCharacterEncoding(encoding);
        PrintWriter out = resp.getWriter();
        UserService userService = new UserServiceImpl();
        List<User> list = userService.queryAll(null);
        for (User u : list){
            out.println(u + "<br>");
        }
    }
}

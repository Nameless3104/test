package day06.action;

import day06.po.User;
import day06.service.UserServiceImpl;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/findUserById.do")
public class FindUserById extends HttpServlet {


    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doPost(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        String encoding = this.getServletContext().getInitParameter("encoding");
        req.setCharacterEncoding(encoding);
        resp.setContentType("text/html;charset=" + encoding);

        int id = Integer.parseInt(req.getParameter("id"));

        User user = new UserServiceImpl().findUserById(id);

        if (user != null){

            req.setAttribute("user", user);
            req.getRequestDispatcher("/day06/updateUser.jsp").forward(req, resp);

        } else {
            resp.sendRedirect("/Day06_war_exploded/day06/login06.jsp"); // 重定向至登录页面
        }

    }
}

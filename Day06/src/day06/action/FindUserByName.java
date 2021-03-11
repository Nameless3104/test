package day06.action;

import day06.po.User;
import day06.service.UserServiceImpl;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

@WebServlet("/findUserByName.do")
public class FindUserByName extends HttpServlet {

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        String encoding = this.getServletContext().getInitParameter("encoding");
        req.setCharacterEncoding(encoding);
        resp.setContentType("text/html;charset=" + encoding);

        String userName = req.getParameter("username");

        boolean flag = new UserServiceImpl().findUserByName(userName);

        PrintWriter out = resp.getWriter();

        if (flag){
            out.println("1");
        } else {
            out.println("0");
        }

    }
}

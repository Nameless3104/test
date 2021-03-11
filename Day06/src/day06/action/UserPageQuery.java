package day06.action;

import day06.po.User;
import day06.service.UserService;
import day06.service.UserServiceImpl;
import day06.utils.PageInfo;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@WebServlet("/userPageQuery.do")
public class UserPageQuery extends HttpServlet {
    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String encoding = this.getServletContext().getInitParameter("encoding");
        req.setCharacterEncoding(encoding);
        resp.setContentType("text/html;charset=" + encoding);

        String pageCurrent = req.getParameter("pageCurrent");
        int pageCurr = 1;
        if (null != pageCurrent){
            pageCurr = Integer.parseInt(pageCurrent);
        }
        PageInfo pageInfo = new PageInfo();
        pageInfo.setPageCurrent(pageCurr);

        UserService userService = new UserServiceImpl();
        List<User> list = userService.queryAllPage(pageInfo, null);
        int totalCount = userService.getTotalCount();
        pageInfo.setTotalCount(totalCount);
        int pageSize = pageInfo.getPageSize();
        int pageCount = (int) Math.ceil((double)totalCount / (double) pageSize);
        pageInfo.setPageCount(pageCount);

        req.setAttribute("list", list);
        req.setAttribute("pageInfo", pageInfo);
        req.getRequestDispatcher("/day06/UserList.jsp").forward(req, resp);

    }
}

package day06.dao;

import day06.po.User;
import day06.utils.PageInfo;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import static day06.utils.BaseDao.*;

public class UserDaoImpl implements UserDao{
    @Override
    public int addUser(User user) {
        var sql = "INSERT INTO tusers VALUES (?, ?, ?);";
        return updateManipulate(sql, user.getaId(), user.getaName(), user.getaPassword());
    }

    @Override
    public int deleteUser(int id) {
        var sql = "DELETE FROM tusers WHERE aid = ?";
        return updateManipulate(sql, id);
    }

    @Override
    public User findUserById(int id) {
        var sql = "SELECT * FROM tusers WHERE aid = ?";
        List<User> list = queryManipulate(sql, id);
        if (!list.isEmpty()){
            return list.get(0);
        } else {
            return null;
        }
    }

    @Override
    public boolean findUserByName(String name) {
        var sql = "SELECT * FROM tusers WHERE aname = ?";
        List<User> list = queryManipulate(sql, name);
        return !list.isEmpty();
    }


    @Override
    public int updateUser(User user) {
        var sql = "UPDATE tusers SET aname = ?,apassword = ? WHERE aid = ?";
        return updateManipulate(sql, user.getaName(), user.getaPassword(), user.getaId());
    }

    @Override
    public List<User> queryAll() {
        var sql = "SELECT * FROM tusers";
        return queryManipulate(sql);
    }

    @Override
    public User login(String username, String password) {
        var sql = "SELECT * FROM tusers WHERE aname = ? AND apassword = ?";
        List<User> list = queryManipulate(sql, username, password);
        if (!list.isEmpty()){
            return list.get(0);
        } else {
            return null;
        }
    }

    @Override
    public List<User> queryAllPage(PageInfo pageInfo, User user) {
        var sql = "SELECT * FROM tusers LIMIT ?,?";
        int begin = (pageInfo.getPageCurrent()-1) * pageInfo.getPageSize();
        int count = pageInfo.getPageSize();
        List<User> list = queryManipulate(sql, begin, count);
        if (!list.isEmpty()){
            return list;
        } else {
            return null;
        }
    }

    @Override
    public int getTotalCount() {
        int i = 0;
        Connection conn = getConnection();
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            var sql = "SELECT count(*) FROM tusers";
            pstmt = conn.prepareStatement(sql);
            rs = pstmt.executeQuery();
            while (rs.next()){
                i = rs.getInt(1);
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        } finally {
            closeAll(conn, pstmt, rs);
        }
        return i;
    }

}

package day06.utils;

import day06.po.User;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Util {
    public static int getMaxId(){
        List<User> list = BaseDao.queryManipulate("SELECT * FROM tusers");
        List<Integer> nums = new ArrayList<Integer>();
        for (User u : list){
            nums.add(u.getaId());
        }
        return Collections.max(nums);
    }
}

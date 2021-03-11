package day06.po;

import day06.utils.Util;

import java.util.LinkedList;

public class User {

    private final static int numOfMaxId = Util.getMaxId();

    private static LinkedList<Integer> list = new LinkedList<Integer>();
    static{
        for (int i = numOfMaxId + 1; i < 100; i++){
            list.add(i);
        }
    }


    private int aId = 0;
    private String aName = "default name";
    private String aPassword = "default password";

    public User() {
    }

    public User(String aName, String aPassword) {
        this.aName = aName;
        this.aPassword = aPassword;
        this.aId = (int) list.removeFirst();
    }

    public User(String aName, String aPassword, int aId) {
        this.aName = aName;
        this.aPassword = aPassword;
        this.aId = aId;
    }

    public String getaName() {
        return aName;
    }

    public void setaName(String aName) {
        this.aName = aName;
    }

    public String getaPassword() {
        return aPassword;
    }

    public void setaPassword(String aPassword) {
        this.aPassword = aPassword;
    }

    public int getaId() {
        return aId;
    }

    public void setaId(int aId) {
        this.aId = aId;
    }

    @Override
    public String toString() {
        return "User{" +
                "aName='" + aName + '\'' +
                ", aPassword='" + aPassword + '\'' +
                ", aId=" + aId +
                '}';
    }
}

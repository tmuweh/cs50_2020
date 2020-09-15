package edu.harvard.cs50.pokedex;

public class Pokemon {
    private String name;
    private String url;

    Pokemon(String name, String url) {
        this.name = name;
        this.url = url;
    }

    public String getName() {
        return name;
    }

    public String getUrl() {
        return url;
    }
}

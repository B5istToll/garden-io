/*
 * Copyright (C) Schweizerische Bundesbahnen SBB, 2016.
 */

package endpoint;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

import hack.gardening.io.web.model.json.Plant;
import services.JasonService;

/*
To let this program run type this in CLI:  mvn package && java -jar ./hack-gardening-io-web/target/hack-gardening-io-web-1.0-SNAPSHOT.jar
 */
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        ApplicationContext ctx = SpringApplication.run(Application.class, args);

        System.out.println("Let's inspect the beans provided by Spring Boot:");

        String[] beanNames = ctx.getBeanDefinitionNames();
        Arrays.sort(beanNames);
        for (String beanName : beanNames) {
            System.out.println(beanName);
        }

        try {
            Path path = Paths.get("hack-gardening-io-web\\src\\main\\java\\data\\plants.json");
            if (Files.exists(path)){
                JasonService jasonService = new JasonService();
                List<Plant> plantList = jasonService.unmarshalJsonObject(path);
                System.out.println(plantList.get(1).getName());
            }

            else
                System.err.println("Input nicht gefunden");
            System.exit(0);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let path = "input";
    println!("Part 1: {}", part1(path));
    println!("Part 2: {}", part2(path));
}

struct ProblemData{
    col1: Vec<i32>,
    col2: Vec<i32>,
}

fn parse_data(path: &str) -> ProblemData {
    let file = File::open(path).unwrap();
    let reader  = BufReader::new(file);
    let mut col1 = vec![];
    let mut col2 = vec![];
    for line in reader.lines() {
        let line = line.unwrap();
        let mut split = line.split_whitespace();

        let item1 = split.next().unwrap().parse::<i32>().unwrap();
        let item2 = split.next().unwrap().parse::<i32>().unwrap();
        col1.push(item1);
        col2.push(item2);
    }
    col1.sort();
    col2.sort();
    ProblemData{col1,col2}
}

fn part1(path: &str) -> u32 {
    let data = parse_data(path);
    let mut total = 0;
    for (x,y) in data.col1.iter().zip(data.col2.iter()) {
        total += x.abs_diff(*y)
    }
    total
}

fn part2(path: &str) -> i32 {
    let data = parse_data(path);
    let mut cache = HashMap::new();
    let mut total = 0;
    for item in data.col1.iter() {
        let val = match cache.contains_key(&item){
            true => {cache.get(&item).unwrap()},
            false => {
                let val = data.col2.iter().filter(|&n| n == item).count() as i32;
                cache.insert(item, val);
                cache.get(&item).unwrap()
            }
        };
        total += item * val;
    }
    total
}
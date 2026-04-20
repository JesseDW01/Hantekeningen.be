import type { Product, PortfolioItem } from '../types/index';
import productsJson from '../data/products.json';
import portfolioJson from '../data/portfolio.json';

export const products: Product[] = productsJson as Product[];
export const portfolioItems: PortfolioItem[] = portfolioJson as PortfolioItem[];

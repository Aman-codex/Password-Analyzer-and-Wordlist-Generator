
import argparse
from generator import generate_candidates
from analyzer import assess_password

def main():
    p = argparse.ArgumentParser(description="Password Strength Analyzer & Custom Wordlist Generator")
    sub = p.add_subparsers(dest='cmd')

    gen = sub.add_parser('generate', help='Generate a wordlist from hints')
    gen.add_argument('-o','--out', default='wordlist.txt')
    gen.add_argument('-m','--max', type=int, default=5000)
    gen.add_argument('hints', nargs='+', help='Hints (name, pet, date, etc)')

    ana = sub.add_parser('analyze', help='Analyze a password')
    ana.add_argument('password', help='Password to analyze')

    args = p.parse_args()

    if args.cmd == 'generate':
        candidates = generate_candidates(args.hints, max_output=args.max)
        with open(args.out, 'w', encoding='utf8') as f:
            for c in candidates:
                f.write(c + '\n')
        print(f'Wrote {len(candidates)} candidates to {args.out}')
    elif args.cmd == 'analyze':
        res = assess_password(args.password)
        print('zxcvbn score (0-4):', res['zxcvbn_score'])
        print('Estimated entropy (bits):', res['estimated_entropy_bits'])
        print('Feedback:', res['zxcvbn_feedback'])
        print('Crack time display:', res['crack_time_display'])
    else:
        p.print_help()

if __name__ == '__main__':
    main()

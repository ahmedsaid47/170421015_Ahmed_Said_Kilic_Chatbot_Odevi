"""
Cullinan Hotel Chatbot - Log Analiz ve Monitoring Aracı
======================================================
Bu araç, chatbot loglarını analiz eder ve detaylı raporlar üretir.

Özellikler:
- Real-time log monitoring
- Performance analizi
- Error pattern detection
- Intent classification analysis
- Response time metrics
- Token usage tracking
- User interaction patterns
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import argparse
import time
import logging

# Grafik için opsiyonel import
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.animation import FuncAnimation
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class LogAnalyzer:
    """Chatbot loglarını analiz eden sınıf"""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.logs = []
        self.load_logs()
    
    def load_logs(self):
        """Log dosyasını yükle ve parse et"""
        if not self.log_file.exists():
            print(f"❌ Log dosyası bulunamadı: {self.log_file}")
            return
        
        print(f"📁 Log dosyası yükleniyor: {self.log_file}")
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    log_entry = json.loads(line)
                    log_entry['line_number'] = line_num
                    self.logs.append(log_entry)
                except json.JSONDecodeError as e:
                    print(f"⚠️ Satır {line_num} parse edilemedi: {e}")
        
        print(f"✅ {len(self.logs)} log kaydı yüklendi")
    
    def get_logs_by_timerange(self, hours_back: int = 24) -> List[Dict]:
        """Belirtilen saat geriye kadar olan logları getir"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        filtered_logs = []
        for log in self.logs:
            try:
                log_time = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
                if log_time >= cutoff_time:
                    filtered_logs.append(log)
            except (KeyError, ValueError):
                continue
        
        return filtered_logs
    
    def get_error_summary(self, hours_back: int = 24) -> Dict[str, Any]:
        """Hata analizi raporu"""
        logs = self.get_logs_by_timerange(hours_back)
        error_logs = [log for log in logs if log.get('level') in ['ERROR', 'CRITICAL']]
        
        error_types = Counter()
        error_contexts = Counter()
        error_modules = Counter()
        
        for log in error_logs:
            # Hata tipi
            if 'exception' in log:
                error_types[log['exception']['type']] += 1
            elif 'error_details' in log:
                error_types[log['error_details'].get('error_type', 'Unknown')] += 1
            
            # Hata konteksti
            if 'error_details' in log:
                error_contexts[log['error_details'].get('context', 'Unknown')] += 1
            
            # Modül
            error_modules[log.get('module', 'Unknown')] += 1
        
        return {
            'total_errors': len(error_logs),
            'error_rate': len(error_logs) / len(logs) * 100 if logs else 0,
            'error_types': dict(error_types.most_common(10)),
            'error_contexts': dict(error_contexts.most_common(10)),
            'error_modules': dict(error_modules.most_common(10)),
            'recent_errors': error_logs[-5:]  # Son 5 hata
        }
    
    def get_performance_summary(self, hours_back: int = 24) -> Dict[str, Any]:
        """Performance analizi raporu"""
        logs = self.get_logs_by_timerange(hours_back)
        performance_logs = [log for log in logs if 'execution_time' in log]
        
        if not performance_logs:
            return {'message': 'Performance verisi bulunamadı'}
        
        # Execution time statistics
        exec_times = [log['execution_time'] for log in performance_logs]
        exec_times.sort()
        
        # Function/operation breakdown
        operation_times = defaultdict(list)
        for log in performance_logs:
            operation = log.get('operation', log.get('event_type', 'unknown'))
            operation_times[operation].append(log['execution_time'])
        
        # Calculate statistics for each operation
        operation_stats = {}
        for op, times in operation_times.items():
            times.sort()
            operation_stats[op] = {
                'count': len(times),
                'avg': sum(times) / len(times),
                'min': min(times),
                'max': max(times),
                'p50': times[len(times)//2],
                'p95': times[int(len(times)*0.95)],
                'p99': times[int(len(times)*0.99)]
            }
        
        return {
            'total_operations': len(performance_logs),
            'avg_execution_time': sum(exec_times) / len(exec_times),
            'min_execution_time': min(exec_times),
            'max_execution_time': max(exec_times),
            'p50_execution_time': exec_times[len(exec_times)//2],
            'p95_execution_time': exec_times[int(len(exec_times)*0.95)],
            'p99_execution_time': exec_times[int(len(exec_times)*0.99)],
            'operation_stats': operation_stats
        }
    
    def get_intent_analysis(self, hours_back: int = 24) -> Dict[str, Any]:
        """Intent sınıflandırma analizi"""
        logs = self.get_logs_by_timerange(hours_back)
        intent_logs = [log for log in logs if log.get('event_type') == 'intent_classification']
        
        if not intent_logs:
            return {'message': 'Intent classification verisi bulunamadı'}
        
        intent_counts = Counter()
        confidence_scores = defaultdict(list)
        low_confidence_intents = []
        
        for log in intent_logs:
            intent = log.get('intent')
            confidence = log.get('confidence', 0)
            
            if intent:
                intent_counts[intent] += 1
                confidence_scores[intent].append(confidence)
                
                if confidence < 0.5:  # Low confidence threshold
                    low_confidence_intents.append({
                        'intent': intent,
                        'confidence': confidence,
                        'user_input': log.get('user_input', ''),
                        'timestamp': log.get('timestamp')
                    })
        
        # Average confidence per intent
        avg_confidence = {}
        for intent, scores in confidence_scores.items():
            avg_confidence[intent] = sum(scores) / len(scores)
        
        return {
            'total_classifications': len(intent_logs),
            'intent_distribution': dict(intent_counts.most_common()),
            'average_confidence_by_intent': avg_confidence,
            'low_confidence_count': len(low_confidence_intents),
            'low_confidence_examples': low_confidence_intents[-10:],  # Son 10 örnek
        }
    
    def get_api_usage_summary(self, hours_back: int = 24) -> Dict[str, Any]:
        """API kullanım analizi"""
        logs = self.get_logs_by_timerange(hours_back)
        api_logs = [log for log in logs if log.get('event_type') == 'api_call_success']
        
        if not api_logs:
            return {'message': 'API kullanım verisi bulunamadı'}
        
        api_counts = Counter()
        total_tokens = 0
        total_cost_estimate = 0
        
        for log in api_logs:
            api_name = log.get('api_name', 'unknown')
            api_counts[api_name] += 1
            
            # Token counting
            prompt_tokens = log.get('prompt_tokens', 0)
            completion_tokens = log.get('completion_tokens', 0)
            total_tokens += prompt_tokens + completion_tokens
            
            # Rough cost estimation (GPT-4o-mini pricing)
            if 'embedding' in api_name.lower():
                total_cost_estimate += (prompt_tokens / 1000) * 0.0001  # $0.0001 per 1K tokens
            else:
                total_cost_estimate += (prompt_tokens / 1000) * 0.00015  # Input
                total_cost_estimate += (completion_tokens / 1000) * 0.0006  # Output
        
        return {
            'total_api_calls': len(api_logs),
            'api_distribution': dict(api_counts.most_common()),
            'total_tokens_used': total_tokens,
            'estimated_cost_usd': round(total_cost_estimate, 4)
        }
    
    def get_user_interaction_summary(self, hours_back: int = 24) -> Dict[str, Any]:
        """Kullanıcı etkileşim analizi"""
        logs = self.get_logs_by_timerange(hours_back)
        conversation_logs = [log for log in logs if log.get('event_type') == 'conversation_start']
        
        if not conversation_logs:
            return {'message': 'Kullanıcı etkileşim verisi bulunamadı'}
        
        # Conversation patterns
        hourly_conversations = defaultdict(int)
        conversation_lengths = defaultdict(int)
        
        for log in conversation_logs:
            try:
                hour = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')).hour
                hourly_conversations[hour] += 1
                
                request_id = log.get('request_id')
                if request_id:
                    # Count messages in this conversation
                    conversation_messages = [l for l in logs if l.get('request_id') == request_id]
                    conversation_lengths[len(conversation_messages)] += 1
            except (KeyError, ValueError):
                continue
        
        return {
            'total_conversations': len(conversation_logs),
            'hourly_distribution': dict(hourly_conversations),
            'conversation_length_distribution': dict(conversation_lengths),
            'avg_conversations_per_hour': len(conversation_logs) / hours_back
        }
    
    def generate_full_report(self, hours_back: int = 24) -> str:
        """Kapsamlı rapor üret"""
        print(f"\n🔍 Son {hours_back} saatlik log analizi başlıyor...")
        
        report = []
        report.append("="*80)
        report.append(f"CULLINAN HOTEL CHATBOT - LOG ANALİZ RAPORU")
        report.append(f"Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Analiz Periyodu: Son {hours_back} saat")
        report.append("="*80)
        
        # Error Analysis
        error_summary = self.get_error_summary(hours_back)
        report.append("\n📊 HATA ANALİZİ")
        report.append("-" * 40)
        report.append(f"Toplam Hata: {error_summary['total_errors']}")
        report.append(f"Hata Oranı: {error_summary['error_rate']:.2f}%")
        
        if error_summary['error_types']:
            report.append("\nEn Sık Hata Tipleri:")
            for error_type, count in list(error_summary['error_types'].items())[:5]:
                report.append(f"  • {error_type}: {count}")
        
        # Performance Analysis
        perf_summary = self.get_performance_summary(hours_back)
        if 'avg_execution_time' in perf_summary:
            report.append("\n⚡ PERFORMANCE ANALİZİ")
            report.append("-" * 40)
            report.append(f"Toplam İşlem: {perf_summary['total_operations']}")
            report.append(f"Ortalama Süre: {perf_summary['avg_execution_time']:.2f}ms")
            report.append(f"P95 Süre: {perf_summary['p95_execution_time']:.2f}ms")
            report.append(f"En Yavaş: {perf_summary['max_execution_time']:.2f}ms")
            
            if perf_summary['operation_stats']:
                report.append("\nİşlem Bazında Performance:")
                for op, stats in list(perf_summary['operation_stats'].items())[:5]:
                    report.append(f"  • {op}: {stats['avg']:.2f}ms (avg), {stats['count']} işlem")
        
        # Intent Analysis
        intent_summary = self.get_intent_analysis(hours_back)
        if 'total_classifications' in intent_summary:
            report.append("\n🎯 INTENT ANALİZİ")
            report.append("-" * 40)
            report.append(f"Toplam Sınıflandırma: {intent_summary['total_classifications']}")
            report.append(f"Düşük Güven Skoru: {intent_summary['low_confidence_count']}")
            
            if intent_summary['intent_distribution']:
                report.append("\nIntent Dağılımı:")
                for intent, count in list(intent_summary['intent_distribution'].items())[:5]:
                    avg_conf = intent_summary['average_confidence_by_intent'].get(intent, 0)
                    report.append(f"  • {intent}: {count} (%{avg_conf:.1f} güven)")
        
        # API Usage
        api_summary = self.get_api_usage_summary(hours_back)
        if 'total_api_calls' in api_summary:
            report.append("\n🌐 API KULLANIMI")
            report.append("-" * 40)
            report.append(f"Toplam API Çağrısı: {api_summary['total_api_calls']}")
            report.append(f"Toplam Token: {api_summary['total_tokens_used']:,}")
            report.append(f"Tahmini Maliyet: ${api_summary['estimated_cost_usd']}")
        
        # User Interactions
        user_summary = self.get_user_interaction_summary(hours_back)
        if 'total_conversations' in user_summary:
            report.append("\n👥 KULLANICI ETKİLEŞİMLERİ")
            report.append("-" * 40)
            report.append(f"Toplam Konuşma: {user_summary['total_conversations']}")
            report.append(f"Saatlik Ortalama: {user_summary['avg_conversations_per_hour']:.1f}")
            
            if user_summary['hourly_distribution']:
                peak_hour = max(user_summary['hourly_distribution'], 
                              key=user_summary['hourly_distribution'].get)
                peak_count = user_summary['hourly_distribution'][peak_hour]
                report.append(f"En Yoğun Saat: {peak_hour}:00 ({peak_count} konuşma)")
        
        report.append("\n" + "="*80)
        return "\n".join(report)


class LogMonitor:
    """Real-time log monitoring"""
    
    def __init__(self, log_file: Path, refresh_interval: int = 5):
        self.log_file = log_file
        self.refresh_interval = refresh_interval
        self.last_position = 0
        self.error_patterns = [
            r"ERROR|CRITICAL",
            r"exception",
            r"failed",
            r"timeout"
        ]
    
    def monitor(self):
        """Log dosyasını real-time takip et"""
        print(f"📺 Log monitoring başlatıldı: {self.log_file}")
        print(f"🔄 Yenileme aralığı: {self.refresh_interval} saniye")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                self.check_new_logs()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            print("\n👋 Monitoring durduruldu")
    
    def check_new_logs(self):
        """Yeni log kayıtlarını kontrol et"""
        if not self.log_file.exists():
            return
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            f.seek(self.last_position)
            new_lines = f.readlines()
            self.last_position = f.tell()
        
        for line in new_lines:
            line = line.strip()
            if not line:
                continue
            
            try:
                log_entry = json.loads(line)
                self.process_log_entry(log_entry)
            except json.JSONDecodeError:
                continue
    
    def process_log_entry(self, log_entry: Dict):
        """Log kaydını işle ve önemli olayları highlight et"""
        level = log_entry.get('level', 'INFO')
        timestamp = log_entry.get('timestamp', '')
        message = log_entry.get('message', '')
        
        # Color coding
        colors = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Green
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',    # Red
            'CRITICAL': '\033[35m'  # Magenta
        }
        reset = '\033[0m'
        
        color = colors.get(level, '')
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            time_str = dt.strftime('%H:%M:%S')
        except:
            time_str = timestamp[:8] if timestamp else '??:??:??'
        
        # Print log entry
        print(f"{color}[{level}]{reset} {time_str} - {message}")
        
        # Additional info for errors
        if level in ['ERROR', 'CRITICAL']:
            if 'error_details' in log_entry:
                print(f"  📝 Details: {log_entry['error_details']}")
            if 'request_id' in log_entry:
                print(f"  🔗 Request ID: {log_entry['request_id'][:8]}...")


def create_sample_dashboard():
    """Basit bir dashboard oluştur (matplotlib varsa)"""
    if not HAS_MATPLOTLIB:
        print("📈 Dashboard özelliği için matplotlib gerekli: pip install matplotlib")
        return
    
    # Bu fonksiyon geliştirilecek - grafik dashboard
    print("📊 Dashboard özelliği geliştirilmekte...")


def main():
    parser = argparse.ArgumentParser(description="Chatbot Log Analiz Aracı")
    parser.add_argument('--log-file', '-f', 
                       default='logs/hotel_chatbot.json.log',
                       help='Log dosyası yolu')
    parser.add_argument('--mode', '-m', 
                       choices=['analyze', 'monitor', 'dashboard'],
                       default='analyze',
                       help='Çalışma modu')
    parser.add_argument('--hours', '-h', 
                       type=int, default=24,
                       help='Analiz edilecek saat sayısı (geriye dönük)')
    parser.add_argument('--output', '-o',
                       help='Raporu dosyaya kaydet')
    parser.add_argument('--refresh', '-r',
                       type=int, default=5,
                       help='Monitor modunda yenileme aralığı (saniye)')
    
    args = parser.parse_args()
    
    log_file = Path(args.log_file)
    
    if args.mode == 'analyze':
        analyzer = LogAnalyzer(log_file)
        report = analyzer.generate_full_report(args.hours)
        
        print(report)
        
        if args.output:
            output_file = Path(args.output)
            output_file.write_text(report, encoding='utf-8')
            print(f"\n💾 Rapor kaydedildi: {output_file}")
    
    elif args.mode == 'monitor':
        monitor = LogMonitor(log_file, args.refresh)
        monitor.monitor()
    
    elif args.mode == 'dashboard':
        create_sample_dashboard()


if __name__ == "__main__":
    main()

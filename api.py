from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import os
import json
from utils.date_utils import get_previous_week_dates, format_week_range
from reports.CV.report_generator import generate_weekly_report as generate_cv_report
from reports.EID.report_generator import generate_weekly_report as generate_eid_report

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/generate-reports', methods=['POST'])
def generate_reports():
    try:
        data = request.get_json() or {}
        
        # Get date range
        if 'start_date' in data and 'end_date' in data:
            start_date = datetime.fromisoformat(data['start_date'])
            end_date = datetime.fromisoformat(data['end_date'])
        else:
            start_date, end_date = get_previous_week_dates()
        
        overwrite = data.get('overwrite', True)
        
        results = {}
        
        # Generate CV Report
        if data.get('generate_cv', True):
            cv_tables = [
                "samples_instruments",
                "vl_samples_backlog", 
                "vl_registered_samples",
                "VL Samples Tested",
                "VL TRL by US",
                "Tempo de Transporte"
            ]
            
            cv_path = generate_cv_report("Carga Viral", cv_tables, start_date, end_date, overwrite)
            results['cv_report'] = {
                "status": "success" if cv_path else "failed",
                "path": cv_path,
                "week_range": format_week_range(start_date, end_date)
            }
        
        # Generate EID Report
        if data.get('generate_eid', True):
            eid_tables = ["EID Data Table 1", "EID Data Table 2"]
            
            eid_path = generate_eid_report("DPI", eid_tables, start_date, end_date, overwrite)
            results['eid_report'] = {
                "status": "success" if eid_path else "failed", 
                "path": eid_path,
                "week_range": format_week_range(start_date, end_date)
            }
        
        return jsonify({
            "success": True,
            "message": "Reports generated successfully",
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/schedule-reports', methods=['POST'])
def schedule_reports():
    """Endpoint para n8n agendar relatórios"""
    return generate_reports()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
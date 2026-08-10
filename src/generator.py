import random
import logging
from typing import List
from .parser import ULPParser, ULPRecord

logger = logging.getLogger(__name__)


class CredentialGenerator:
    """Generate credentials from search results"""

    @staticmethod
    def generate(records: List[ULPRecord], quantity: int = 1, 
                output_format: str = 'WITH_URL', random_selection: bool = True) -> List[str]:
        """
        Generate credentials from records
        
        Args:
            records: List of ULPRecord objects
            quantity: Number of credentials to generate
            output_format: Format of output (WITH_URL, WITHOUT_URL, URL_ONLY, LOGIN_ONLY)
            random_selection: Whether to randomly select or take first N
        
        Returns:
            List of formatted credential strings
        """
        if not records:
            return []

        # Ensure quantity doesn't exceed available records
        quantity = min(quantity, len(records))

        # Select records
        if random_selection:
            selected = random.sample(records, quantity)
        else:
            selected = records[:quantity]

        # Format records
        formatted = []
        for record in selected:
            formatted_record = ULPParser.format_record(record, output_format)
            if formatted_record:
                formatted.append(formatted_record)

        return formatted

    @staticmethod
    def generate_with_duplicates_protection(records: List[ULPRecord], quantity: int = 1,
                                           output_format: str = 'WITH_URL') -> List[str]:
        """Generate without duplicate credentials"""
        if not records:
            return []

        quantity = min(quantity, len(records))

        # Format and remove duplicates
        seen = set()
        result = []

        random_records = random.sample(records, min(len(records), quantity * 2))

        for record in random_records:
            formatted = ULPParser.format_record(record, output_format)
            if formatted and formatted not in seen:
                seen.add(formatted)
                result.append(formatted)
                if len(result) >= quantity:
                    break

        return result[:quantity]

    @staticmethod
    def preview_generation(records: List[ULPRecord], quantity: int = 1,
                          output_format: str = 'WITH_URL') -> str:
        """Generate preview of credentials"""
        generated = CredentialGenerator.generate(records, quantity, output_format)
        
        preview = f"📋 **Generation Preview**\n"
        preview += f"Format: {output_format}\n"
        preview += f"Quantity: {len(generated)}\n"
        preview += f"Available: {len(records)}\n"
        preview += f"\n"

        if generated:
            preview += "**Sample (first 5):**\n"
            for idx, cred in enumerate(generated[:5], 1):
                preview += f"{idx}. `{cred}`\n"
            
            if len(generated) > 5:
                preview += f"\n... and {len(generated) - 5} more"
        else:
            preview += "No credentials to preview"

        return preview

    @staticmethod
    def generate_batch(records: List[ULPRecord], quantities: dict, 
                      output_format: str = 'WITH_URL') -> dict:
        """Generate multiple batches"""
        results = {}
        for name, qty in quantities.items():
            results[name] = CredentialGenerator.generate(records, qty, output_format)
        return results
